import json
import os
from datetime import date, timedelta, datetime, timezone

from dateutil.relativedelta import relativedelta

from common.rails_context import RailsContext, railway
from services.data_service import DataService


class DiagramMaker:


	#==============================================
	@railway
	def update_diagram(self, context: RailsContext, cpath, dpath: str):
		if not os.path.exists(dpath):
			return context.setError({}, f"Diagram folder does not exist: {dpath}")

		tasks = self._get_tasks_list(context, cpath)
		self._make_jsfile(context, tasks, dpath)


		return True

	#------------------------------------------
	@railway
	def _get_tasks_list(self, context: RailsContext, path):
		ds = DataService()
		ds.load_calendar(context, path)
		return ds.get_all_tasks(context)

	#------------------------------------------
	@railway
	def _make_jsfile(self, context: RailsContext, tasks, path):
		tlist = []
		statuses = []
		for t in tasks:
			if t.status != "Done" and t._is_hidden(): continue
			eid = ",".join(t.external) if t.external else "-"
			next = t.next if t.next else "-"
			due = t.due_text if t.due_text else "-"
			age = self._get_task_age(t)
			size = self._get_task_size(t)
			item = {
				"Title": t.title,
				"EID": eid,
				"Size": f"{size}",
				"Project": t.project,
				"Status": t.status,
				"Created": t.created_text,
				"Due date": due,
				"Priority": t.priority,
				"Next": next,
				"Age": f"{age}",
				"Time left": f"{t.remains}"
			}
			tlist.append(item)
			if not t.status in statuses: statuses.append(t.status)

		if not 'Done' in statuses: self._add_small(tlist, "completed", "Done")
		if not 'Overdue' in statuses: self._add_small(tlist, "overdue", "Overdue")
		if not 'Urgent' in statuses: self._add_small(tlist, "urgent", "Urgent")
		if not 'Active' in statuses: self._add_small(tlist, "in progress", "Active")
		if not 'Optional' in statuses: self._add_small(tlist, "optional", "Optional")
		if not 'Open' in statuses: self._add_small(tlist, "not started", "Open")

		text = "modelDataAvailable("
		text += json.dumps(tlist, indent=2)
		text += ")"
		with open(path, "w") as text_file:
			text_file.write(text)
		return True

	#------------------------------------------
	def _add_small(self, tlist, title, status):
		tlist.append({
			"Title": title,
			"EID": "US",
			"Size": "0.1",
			"Project": "",
			"Status": status,
			"Created": "2026-05-01",
			"Due date": "-",
			"Priority": "Year",
			"Next": "-",
			"Age": "10",
			"Time left": "10"
		})

	#------------------------------------------
	def _get_task_size(self, task):
		if not task.size: return 1;
		match task.size:
			case "2": return 2
			case "3": return 4
			case "4": return 8
			case "5": return 10
			case "6": return 16
			case "7": return 24
			case _: return 1



	#------------------------------------------
	def _get_task_age(self, task):
		res = 10
		if not task.remains: return 10
		if task.remains < 2: return 100
		if task.remains < 3: return 80
		if task.remains < 4: return 70
		if task.remains < 5: return 60
		if task.remains < 6: return 50
		if task.remains < 7: return 40
		if task.remains < 8: return 30
		if task.remains < 9: return 20
		if task.remains < 10: return 10
		if task.remains < 12: return 8
		if task.remains < 15: return 6
		if task.remains < 22: return 5
		if task.remains < 30: return 4
		if task.remains < 45: return 3
		if task.remains < 90: return 2
		return 1



	#------------------------------------------
	def _clean_title(self, text):
		res = ""
		for ch in text:
			if ch == ' ': res += ' '
			if ch.isalnum(): res += ch
		return res

	#------------------------------------------
	def _create_id(self, text):
		res = ""
		for ch in text:
			if ch.isalnum(): res += ch
		return res

