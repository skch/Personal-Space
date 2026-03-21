from flask import Blueprint, render_template, current_app, abort, request, redirect, url_for

from common.rails_context import RailsContext
from services.data_service import DataService

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/')
def calendar_page():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	eventlist = service.get_events(context, days=3)
	if context.hasError():
		return render_template('error.html', data=context)
	return render_template('calendar.html', logo = settings.name, days_events=eventlist)



@calendar_bp.route('/<event_id>/edit', methods=['GET', 'POST'])
def event_edit(event_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	event = service.get_event_by_id(context, event_id)
	if request.method == 'POST':
		service.update_event(context, request.form)
		if not context.hasError():
			return redirect(url_for('calendar.calendar_page'))
	if not context.hasError():
		return render_template('event_edit.html', logo = settings.name, event=event)
	return render_template('error.html', data=context)


@calendar_bp.route('/<event_id>/move')
def event_move(event_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	service.move_event(context, event_id)
	if not context.hasError(): return redirect(url_for('calendar.calendar_page'))
	return render_template('error.html', data=context)

@calendar_bp.route('/<event_id>/next')
def event_next(event_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	service.create_next_event(context, event_id)
	if not context.hasError(): return redirect(url_for('calendar.calendar_page'))
	return render_template('error.html', data=context)
