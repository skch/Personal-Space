import os
from collections import defaultdict
import frontmatter
from datetime import date, timedelta, datetime, timezone
from common.rails_context import railway, RailsContext
from services.config_tools import make_event_date_time, make_date_text, make_datetime_text
from services.content_parser import parse_markdown_file
from services.event_wrapper import EventWrapper
from services.markdown_writer import MarkdownWriter
from services.task_wrapper import TaskWrapper


class DataService:

	#==============================================
	@railway
	def load_calendar(self, context: RailsContext, path: str):
		if not os.path.exists(path):
			return context.setError({}, f"Calendar folder does not exist: {path}")

		self.base_path = path
		self.days = {}
		self.tasks = {}
		days = os.listdir(path)
		for dayfolder in days:
			if not self._is_day_folder(dayfolder): continue
			day = self._read_day_content(context, dayfolder)
			self._sort_events(context, day)
			self.days[dayfolder] = day
		return True

	#------------------------------------
	def _is_day_folder(self, name):
		if not os.path.isdir(os.path.join(self.base_path, name)): return False
		if len(name) != 9: return False
		if not name[4] == '-': return False
		return True

	#------------------------------------
	@railway
	def _read_day_content(self, context: RailsContext, name):
		res = {
			"date": name,
			"events": []
		}
		fullpath = os.path.join(self.base_path, name)
		list = os.listdir(fullpath)
		is_today = name == date.today().strftime("%Y-%m%d")
		for filename in list:
			if self._is_event(filename):
				event = self._read_event(context, fullpath, filename)
				res['events'].append(event)
			if self._is_task(filename):
				task = self._read_task(context, fullpath, filename)
				task.prepare_for_display()
				if is_today or task.status != 'Done': self.tasks[task.id] = task
		return res

	#------------------------------------
	@railway
	def get_events(self, context: RailsContext, days):
		cdate = date.today()
		cnt = 1
		res = []
		while cnt <= days:
			name = cdate.strftime("%Y-%m%d")
			if name in self.days:
				day = self.days[name]
				day['title'] = cdate.strftime("%b %d | %a")
				day['color'] = self._get_day_color(cdate)
				res.append(day)
				cnt += 1
			cdate = cdate + timedelta(days=1)
		return res

	#------------------------------------
	@railway
	def get_event_by_id(self, context: RailsContext, eid):
		if eid == 'new': return EventWrapper({}, '', '', '', '')
		fid = eid[:9]
		if not fid in self.days: return context.setError({}, f"Day not found: {fid}")
		day = self.days[fid]
		for event in day['events']:
			if event.id == eid: return event
		return context.setError({}, f"Event not found: {eid}")

	#------------------------------------
	@railway
	def move_event(self, context: RailsContext, eid):
		event = self.get_event_by_id(context, eid)
		self.forward_date(context, event)
		self.delete_event(context, event)
		self.save_event(context, event)

	#------------------------------------
	@railway
	def create_next_event(self, context: RailsContext, eid):
		event = self.get_event_by_id(context, eid)
		self.delete_event(context, event)
		self.save_event(context, event, True)
		self.forward_date(context, event)
		self.save_event(context, event)

	#------------------------------------
	@railway
	def forward_date(self, context: RailsContext, event):
		if not event.repeats: return False
		success = False
		if event.repeats == 'daily' or event.repeats == '1 day':
			event.date = event.date + timedelta(days=1)
			success = True
		if event.repeats == 'weekly' or event.repeats == '1 week':
			event.date = event.date + timedelta(weeks=1)
			success = True
		if not success: return context.setError(False, f"Unknown repeats type: {event.repeats}")

	#------------------------------------
	@railway
	def delete_event(self, context: RailsContext, event):
		if event.path: os.remove(event.path)

	#------------------------------------
	@railway
	def save_event(self, context: RailsContext, event, completed=False):
		title = event.title
		if completed: title += ' ✓'
		fname = self.clean_text(title)
		event_path = self.make_path_for_day(event.date)
		event.path = os.path.join(event_path, event.time.strftime("%H%M")+f' - {fname}.md')

		md = MarkdownWriter()
		md.add("title", title)
		md.add("date", make_date_text(event.date))
		md.add("time", make_datetime_text(event.date, event.time))
		md.add("duration", event.duration)
		md.add("size", event.size)
		md.add("organizer", event.organizer)
		md.add("repeats", event.repeats)
		md.set_tags(event.tags)
		md.body = event.content
		md.save(event.path)

	#------------------------------------
	def update_event(self, context, fdata):
		event = EventWrapper(fdata, fdata.get('content'), '', '', fdata.get('fullname'))
		event.prepare_for_display()
		self._form_to_tags(fdata, event, 'calendar')
		oldname = fdata.get('path')
		if oldname: os.remove(oldname)
		self.save_event(context, event)
		return event

	#------------------------------------
	def _is_event(self, filename):
		if not filename.endswith('.md'): return False
		if filename.startswith('TODO - '): return False
		if filename.startswith('DONE - '): return False
		return True

	#------------------------------------
	def _is_task(self, filename):
		if not filename.endswith('.md'): return False
		if filename.startswith('TODO - '): return True
		if filename.startswith('DONE - '): return True
		return False

	#------------------------------------
	@railway
	def _read_event(self, context, fullpath, filename):
		filepath = os.path.join(fullpath, filename)
		parsed = parse_markdown_file(filepath)
		if parsed:
			event = EventWrapper(parsed['metadata'], parsed['raw_content'], parsed['html'], filename, filepath)
			event.prepare_for_display()
			return event

	#------------------------------------
	@railway
	def _read_task(self, context, fullpath, filename):
		filepath = os.path.join(fullpath, filename)
		parsed = parse_markdown_file(filepath)
		if parsed:
			task = TaskWrapper(parsed['metadata'], parsed['raw_content'], parsed['html'], filename, filepath)
			return task
		return context.setError({}, f"Failed to parse task file: {filepath}")

	#==============================================
	@railway
	def get_grouped_tasks(self, context: RailsContext):
		grouped_tasks = defaultdict(list)
		for tid, t in self.tasks.items():
			grouped_tasks[t.priority].append(t)
		res = {}
		if 'Today' in grouped_tasks: res['Today'] = grouped_tasks['Today']
		if 'Week' in grouped_tasks: res['Week'] = grouped_tasks['Week']
		if 'Month' in grouped_tasks: res['Month'] = grouped_tasks['Month']
		if 'Year' in grouped_tasks: res['Year'] = grouped_tasks['Year']
		return res

	#==============================================
	@railway
	def get_task_by_id(self, context, task_id):
		if task_id == 'new':
			task = TaskWrapper({}, '', '', '', '')
			task.prepare_for_display()
			return task
		return self.tasks.get(task_id)

	#------------------------------------
	def _get_day_color(self, cdate):
		today = date.today()
		if today.isocalendar()[:2] == cdate.isocalendar()[:2]:
			return 'primary'
		return 'info'


	#------------------------------------
	@railway
	def _sort_events(self, context, day):
		list = day['events']
		day['events'] = sorted(list, key=lambda event: event.start)
		return True

	#==============================================
	@railway
	def close_task(self, context, task_id):
		if not task_id in self.tasks: return context.setError({}, f"Task not found: {task_id}")
		task = self.tasks.get(task_id)
		self.mark_closed(context, task)
		self.save_task(context, task)

	#------------------------------------
	@railway
	def mark_closed(self, context, task):
		task.status = 'Done'
		return task

	#------------------------------------
	@railway
	def save_task(self, context, task):
		md = MarkdownWriter()
		try:
			md.add("title", task.title)
			md.add("created", make_date_text(task.created))
			md.add("priority", task.priority)
			md.add("due", make_date_text(task.due))
			md.add("next", task.next)
			md.add("project", task.project)
			md.add("status", task.status)
			md.add("JIRA", task.JIRA)
			md.set_tags(task.tags)
			md.body = task.content
			oldfilename = task.path
			if oldfilename:	os.remove(oldfilename)
			fname = self.clean_text(task.title)
			filepath = self.make_path_for_day(date.today())
			prefix = 'TODO'
			if task.status == 'Done': prefix = 'DONE'
			filename = os.path.join(filepath, f'{prefix} - {fname}.md')
			md.save(filename)
		except Exception as e:
			print(e)
			return context.setException([], f"Cannot save task.", e)

	#------------------------------------
	def update_task(self, context, fdata):
		task = TaskWrapper(fdata, fdata.get('content'), '', '', fdata.get('fullname'))
		task.prepare_for_display()
		self._form_to_tags(fdata, task, 'todo')
		self.save_task(context, task)
		return task


	#------------------------------------
	def clean_text(self, text):
		return text.replace('\\', '-').replace(':', '').replace('/', '-').replace('"', '').replace("'", '')

	#------------------------------------
	def check_on(self, data, checkbox):
		val = data.get(checkbox)
		return val == 'on'

	def make_path_for_day(self, dt):
		path = os.path.join(self.base_path, dt.strftime("%Y-%m%d"))
		os.makedirs(path, exist_ok=True)
		return path

	def _form_to_tags(self, fdata, item, typetag):
		if not item.tags: item.tags = [typetag]
		if self.check_on(fdata, 'icon_quest'): item.tags.append('question')
		if self.check_on(fdata, 'icon_person'): item.tags.append('person')
		if self.check_on(fdata, 'icon_call'): item.tags.append('call')
		if self.check_on(fdata, 'icon_imp'): item.tags.append('important')

