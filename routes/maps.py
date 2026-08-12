from flask import Blueprint, render_template, current_app, abort, request, redirect, url_for

from common.rails_context import RailsContext
from services.data_service import DataService
from services.diagram_maker import DiagramMaker
from services.page_tools import get_header

maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/')
def map_page():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Projects')

	dm = DiagramMaker()
	dm.update_diagram(context, settings.calendar_path, settings.diagram_path)

	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	eventlist = service.get_all_events(context)
	if context.hasError():
		return render_template('error.html', header = head, data=context)
	return render_template('foam.html', header = head, days_events=eventlist)

