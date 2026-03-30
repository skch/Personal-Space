from datetime import date, timedelta, datetime, timezone

from services.config_tools import make_datetime_text
from services.file_wrapper import FileWrapper


class EventWrapper(FileWrapper):

	#----------------------------------
	def __init__(self, item, raw, html, name, path):
		self.data = item
		self.content = raw
		self.html = html
		self.name = name
		self.path = path
		self.date = self._get_as_date('date')
		time = self._get_time()
		self.time = datetime.combine(self.date, time.time())

		self.id = self.time.strftime("%Y-%m%d-%H%M")
		self.start = self.time.timestamp()
		self.title = self.data.get('title', '')
		self.tags = self.data.get('tags', ['calendar'])
		self.status = ''
		self.start = ''
		self.until = ''
		self.tag_imp = ''
		self.tag_quest = ''
		self.tag_person = ''
		self.tag_call = ''


	#==============================================
	def prepare_for_display(self):
		self.repeats = self.get('repeats')
		self.duration = self._get_duration()
		self.organizer = self.get('organizer', '')
		self.client = self.get('client', '')
		self.size = self.get('size', 'Small')

		self._set_tags_checkboxes()
		self.date_text = self._get_date_text(self.date)
		self.start = self.time.strftime("%H:%M")
		self.start_time = self.time.timestamp()
		#self.start_time = self.start_time - 60 * 60  # DST???
		self.end_time = self.start_time + self.duration * 60
		self.status = self._get_status()
		self.until = self._get_time_left()
		self.icons = self._get_repeats() + self._get_icons()
		self.color = self._get_color()

	#----------------------------------
	def _get_status(self):
		now = datetime.now()
		nowtc = now.timestamp()
		if nowtc > self.start_time and nowtc < self.end_time: return 'active'
		return ''

	#----------------------------------
	def _get_color(self):
		match self.size:
			case 'Small': return 'danger'
			case 'Large': return 'primary'
		return 'warning'

	#----------------------------------
	def _get_time_left(self):
		today_date = date.today()
		if self.time.date() == today_date:
			now = datetime.now()
			nowtc = now.timestamp()
			if self.end_time < nowtc:	return f"ended"
			if self.start_time < nowtc:
				total_seconds_left = self.end_time - nowtc
				minutes_left = int(total_seconds_left // 60)
				return f"ends in {minutes_left} min"

			total_seconds_left = self.start_time - nowtc
			minutes_left = int(total_seconds_left // 60)
			return f"in {minutes_left} min"
		else:
			return self.organizer

	#----------------------------------
	def _get_duration(self):
		value = self.data.get('duration')
		if not value: return 60
		if isinstance(value, str): return int(value)
		return value

	#----------------------------------
	def _get_time(self):
		value = self.data.get('time')
		if not value: return datetime.now()
		if isinstance(value, str):
			if len(value) < 6: return datetime.strptime(value, "%H:%M")
			return datetime.fromisoformat(value)
		return value

	# ------------------------------------
	def _get_repeats(self):
		if not self.repeats: return ''
		if self.repeats == '1 day' or self.repeats == 'daily': return '♷'
		if self.repeats == '1 week' or self.repeats == 'weekly': return '♳'
		return '♺'

