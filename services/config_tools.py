import json
import os
from datetime import datetime
import pytz
from common.rails_context import RailsContext, railway

class ConfigTools:
	def __init__(self):
		self.name = "PA System"
		self.version = "1.0.36"


	#==============================================
	@railway
	def load_config(self, context: RailsContext, config_path):
		if not os.path.exists(config_path):
			return context.setError({}, f"Missing config file {config_path}")

		data = {}
		with open(config_path, 'r') as f:
			config_data = json.load(f)
			if 'logo' in config_data: self.name = config_data['logo']
			if not 'wiki' in config_data: return context.setError({}, f"Wiki path is missing")
			if not 'calendar' in config_data: return context.setError({}, f"Calendar path is missing")
			if not 'contacts' in config_data: return context.setError({}, f"Contacts path is missing")
			self.wiki_path = config_data['wiki']
			self.calendar_path = config_data['calendar']
			self.contacts_path = config_data['contacts']
			return True



def get_time_zone():
	timezone_name = 'America/New_York'
	try:
		return pytz.timezone(timezone_name)
	except pytz.UnknownTimeZoneError:
		print(f"Error: Unknown timezone '{timezone_name}'. You can find valid timezones in the pytz.all_timezones list.")
		exit()

def make_event_date_time(tdate, ttime):
	try:
		text = tdate + ' ' + ttime
		dt = datetime.strptime(text, '%Y-%m-%d %H:%M')
		return dt
	except pytz.UnknownTimeZoneError:
		print(f"Error: Invalid datetime '{text}'.")
		exit()

def make_date_text(dt):
	try:
		if not dt: return ''
		if isinstance(dt, str): dt = datetime.strptime(dt, "%Y-%m-%d")
		return dt.strftime("%Y-%m-%d")
	except Exception as e:
		print (e)
		print(f"Error: Invalid date '{dt}'.")
		exit()

def make_datetime_text(dt, tm):
	try:
		return dt.strftime("%Y-%m-%d")+' '+tm.strftime("%H:%M:%S%z")
	except Exception as e:
		print(f"Error: Invalid datetime '{dt} {tm}'.")
		exit()
