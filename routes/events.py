from flask import Blueprint, render_template, current_app, abort, request, redirect, url_for

from common.rails_context import RailsContext
from services.data_service import DataService
from services.diagram_maker import DiagramMaker
from services.page_tools import get_header

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def events_page():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Calendar')
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	eventlist = service.get_all_events(context)
	if context.hasError():
		return render_template('error.html', header = head, data=context)
	return render_template('events.html', header = head, days_events=eventlist)

@events_bp.route('/clean')
def events_clean():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Calendar')
	service = DataService()
	service.clean_days(context, settings.calendar_path)
	if context.hasError():
		return render_template('error.html', header=head, data=context)
	return redirect(url_for('events.events_page'))

@events_bp.route('/compress')
def events_compress():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Calendar')
	service = DataService()
	service.compress_month(context, settings.calendar_path)
	if context.hasError():
		return render_template('error.html', header=head, data=context)
	return redirect(url_for('events.events_page'))

@events_bp.route('/diagram')
def events_diagram():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Calendar')
	service = DiagramMaker()
	service.update_diagram(context, settings.calendar_path, settings.diagram_path)
	if context.hasError():
		return render_template('error.html', header=head, data=context)
	return redirect(url_for('maps.map_page'))

