from datetime import date, timedelta, datetime, timezone

class FileWrapper:

	# ------------------------------------
	def get(self, name, dvalue = ''):
		value = self.data.get(name, dvalue)
		if not value: return dvalue
		return value

	# ------------------------------------
	def _get_icons(self):
		txt = ''
		if not self.tags: return txt
		if 'important' in self.tags: txt += '❗'
		if 'question' in self.tags: txt += '❓'
		if 'person' in self.tags: txt += '👨️'
		if 'call' in self.tags: txt += '📞'
		return txt

	# ------------------------------------
	def _set_tags_checkboxes(self):
		if not self.tags: return
		if 'important' in self.tags: self.tag_imp = 'checked="yes"'
		if 'question' in self.tags: self.tag_quest = 'checked="yes"'
		if 'person' in self.tags: self.tag_person = 'checked="yes"'
		if 'call' in self.tags: self.tag_call = 'checked="yes"'

	#----------------------------------
	def _get_as_date(self, name, default_today = True):
		dvalue = ''
		if default_today: dvalue = datetime.today()
		value = self.data.get(name)
		if not value: return dvalue
		if isinstance(value, str): return datetime.strptime(value, "%Y-%m-%d")
		return value

