import hashlib
from datetime import date, timedelta, datetime, timezone
from services.config_tools import make_date_text
from services.file_wrapper import FileWrapper


class TaskWrapper(FileWrapper):

	#----------------------------------
	def __init__(self, item, content, html, name, path):
		self.data = item
		self.name = name
		self.html = html
		self.path = path
		self.tags = self.data.get('tags', ['todo'])
		self.content = content
		self.id = hashlib.md5(self.path.encode('utf-8')).hexdigest()
		self.tag_important = ''
		self.tag_quest = ''
		self.tag_person = ''
		self.tag_call = ''

	#==============================================
	def prepare_for_display(self):
		dt = make_date_text(datetime.today())
		self.title = self.get('title')
		self.status = self.get('status', 'Open')
		self.priority = self.get('priority', 'Open')
		self.due = self._get_as_date('due', False)
		self.created = self._get_as_date('created')
		self.project = self.get('project', '')
		self.category = self.get('category', '')
		self.next = self.get('next', '')
		self._get_external()
		self.tags = self.data.get('tags', [])

		self._set_tags_checkboxes()
		self.bg_color = self._get_bg_color()
		self.icons = self._get_atticon()+self._get_icons()
		self.remains = self._get_remains()
		self.age = self._get_age()


	# ------------------------------------
	def _get_bg_color(self):
		match self.status:
			case 'Open':
				return 'action'
			case 'Urgent':
				return 'warning'
			case 'Overdue':
				return 'danger'
			case 'Active':
				return 'primary'
			case 'Optional':
				return 'light'
			case 'Ready':
				return 'dark'
			case 'Pending':
				return 'secondary'
			case 'Done':
				return 'success'
			case _:
				return 'action'

	# ------------------------------------
	def _get_remains(self):
		if not self.due: return ''
		cdate = self.due
		if isinstance(cdate, datetime): cdate = cdate.date()
		diff = cdate - date.today()
		return diff.days

	# ------------------------------------
	def _get_age(self):
		if not self.created: return ''
		cdate = self.created
		if isinstance(cdate, datetime): cdate = cdate.date()
		diff = date.today() - cdate
		if diff.days > 365: return f"{diff.days // 365} yr"
		if diff.days > 30: return f"{diff.days // 30} mo"
		if diff.days > 7: return f"{diff.days // 7} wk"
		return f'{diff.days} d'

	# ------------------------------------
	def _get_atticon(self):
		if not self.external: return ''
		return '⬩'

	def _get_external(self):
		value = self.data.get('external', '')
		if not value:
			self.external = []
			self.external_text = ''
			return
		if isinstance(value, list):
			clist = [x for x in value if x is not None]
			self.external = clist
			self.external_text = '; '.join(clist)
		else:
			self.external_text = value
			self.external = self.external_text.split(';')


