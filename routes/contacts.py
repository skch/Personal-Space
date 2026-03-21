import os
from flask import Blueprint, render_template, current_app, send_from_directory, abort
from common.rails_context import RailsContext
from services.people_service import PeopleService

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/')
def contacts_list():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = PeopleService()
	service.load_contacts(context, settings.contacts_path)
	grouped_contacts = service.get_by_group(context)
	if context.hasError():
		return render_template('error.html', data=context.error)
	return render_template('contacts.html', logo = settings.name, grouped_contacts=grouped_contacts)


@contacts_bp.route('/<contact_id>')
def contact_detail(contact_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = PeopleService()
	service.load_contacts(context, settings.contacts_path)
	contact = service.get_by_id(context, contact_id)
	if context.hasError():
		return render_template('error.html', data=context.error)
	return render_template('contact_detail.html', logo = settings.name, contact=contact)


@contacts_bp.route('/<contact_id>/image/<filename>')
def contact_image(contact_id, filename):
	settings = current_app.config['SETTINGS']
	contact_path = os.path.join(settings.contacts_path, contact_id)
	return send_from_directory(contact_path, filename)
