import os
from flask import Blueprint, render_template, current_app, send_from_directory, abort
from common.rails_context import RailsContext
from services.people_service import PeopleService

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/')
def contacts_list():
	context = RailsContext()
	service = PeopleService()
	contacts_folder = current_app.config.get('CONTACTS_FOLDER', './data/contacts')
	service.load_contacts(context, contacts_folder)
	grouped_contacts = service.get_by_group(context)
	if context.hasError():
		return render_template('error.html', data=context.error)
	return render_template('contacts.html', grouped_contacts=grouped_contacts)


@contacts_bp.route('/<contact_id>')
def contact_detail(contact_id):
	context = RailsContext()
	service = PeopleService()
	contacts_folder = current_app.config.get('CONTACTS_FOLDER', './data/contacts')
	service.load_contacts(context, contacts_folder)
	contact = service.get_by_id(context, contact_id)
	if context.hasError():
		return render_template('error.html', data=context.error)
	return render_template('contact_detail.html', contact=contact)


@contacts_bp.route('/<contact_id>/image/<filename>')
def contact_image(contact_id, filename):
	contacts_folder = current_app.config.get('CONTACTS_FOLDER', './data/contacts')
	contact_path = os.path.join(contacts_folder, contact_id)
	return send_from_directory(contact_path, filename)
