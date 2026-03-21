import json
import os
from datetime import datetime
import pytz
from common.rails_context import RailsContext


def copy_config_item(context, src, target, name, app_name):
	if context.hasError(): return False
	if not name in src:
		return context.setError({}, f"Missing {name} folder in config file")
	target[app_name] = src[name]
	return True


def read_config(context: RailsContext, config_path):
	if not os.path.exists(config_path):
		return context.setError({}, f"Missing config file")

	data = {}
	with open(config_path, 'r') as f:
		config_data = json.load(f)
		copy_config_item(context, config_data, data, 'wiki', 'WIKI_FOLDER')
		copy_config_item(context, config_data, data, 'calendar', 'CALENDAR_FOLDER')
		copy_config_item(context, config_data, data, 'contacts', 'CONTACTS_FOLDER')
		return data


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
