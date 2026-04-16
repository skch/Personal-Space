from flask import Blueprint, render_template, current_app, abort, request, redirect, url_for
from common.rails_context import RailsContext
from services.data_service import DataService
from services.page_tools import get_header

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def tasks_list():
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Tasks')
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	grouped_tasks= service.get_grouped_tasks(context)
	if context.hasError():
		return render_template('error.html', header = head, data=context)
	return render_template('tasks.html', header = head, grouped_tasks=grouped_tasks)

@tasks_bp.route('/<task_id>')
def task_detail(task_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Task')
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	task = service.get_task_by_id(context, task_id, "")
	if context.hasError():
		return render_template('error.html', header = head, data=context)
	return render_template('task_detail.html', header = head, task=task)

@tasks_bp.route('/<task_id>/edit', methods=['GET', 'POST'])
def task_edit(task_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Edit Task')
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	priority = request.args.get('priority', default='Day')
	task = service.get_task_by_id(context, task_id, priority)
	if request.method == 'POST':
		service.update_task(context, request.form)
		if not context.hasError():
			return redirect(url_for('tasks.tasks_list', task_id=task_id))
	if not context.hasError():
		return render_template('task_edit.html', header = head, task=task)
	return render_template('error.html', header = head, data=context)

@tasks_bp.route('/<task_id>/close')
def task_close(task_id):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Tasks')
	service = DataService()
	service.load_calendar(context, settings.calendar_path)
	task = service.close_task(context, task_id)
	if not context.hasError(): return redirect(url_for('tasks.tasks_list'))
	return render_template('error.html', header = head, data=context)


