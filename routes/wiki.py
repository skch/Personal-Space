import os
from flask import Blueprint, render_template, current_app, abort, send_from_directory, request, redirect, url_for
from markupsafe import Markup

from common.rails_context import RailsContext
from services.content_parser import parse_markdown_file
from services.page_tools import get_header
from services.wiki_page import WikiPage

wiki_bp = Blueprint('wiki', __name__)


@wiki_bp.route('/edit/<path:path>', methods=['GET', 'POST'])
def wiki_edit(path):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Wiki')
	service = WikiPage()

	safe_path = os.path.normpath(path)
	mdpath, isMD = service.get_page_path(context, settings.wiki_path, safe_path)

	if not isMD:
		if os.path.isfile(mdpath) and not mdpath.endswith('.md'):
			safe_path = safe_path.replace('\\', '/')
			return send_from_directory(settings.wiki_path, safe_path)

	if request.method == 'POST':
		mdtext = request.form['page_text']
		service.save_page(context, mdpath, mdtext)
		return redirect(url_for('wiki.wiki_page', path=path))
	service.load_page(context, mdpath)
	mdata = Markup(service.markdown)
	if context.hasError():
		return render_template('error.html', header = head, data=context)
	return render_template('wiki_edit.html',
												 header = head, raw_content=mdata, metadata=service.metadata, path=path)


@wiki_bp.route('/blocks/<path:path>', methods=['GET', 'POST'])
def wiki_blocks(path):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Wiki')
	service = WikiPage()

	safe_path = os.path.normpath(path)
	mdpath, isMD = service.get_page_path(context, settings.wiki_path, safe_path)

	if not isMD:
		if os.path.isfile(mdpath) and not mdpath.endswith('.md'):
			safe_path = safe_path.replace('\\', '/')
			return send_from_directory(settings.wiki_path, safe_path)

	if request.method == 'POST':
		body = request.form['jsonpage']
		service.save_block_page(context, mdpath, body)
		return redirect(url_for('wiki.wiki_page', path=path))
	service.load_page(context, mdpath)
	mdata = Markup(service.mdata)
	if context.hasError():
		return render_template('error.html', header = head, data=context.error)
	return render_template('wiki_block_edit.html',
												 header = head, raw_content=mdata, metadata=service.metadata, path=path)



@wiki_bp.route('/', defaults={'path': 'Home'})
@wiki_bp.route('/<path:path>')
def wiki_page(path):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	head = get_header(settings, 'Wiki')
	service = WikiPage()
	safe_path = os.path.normpath(path)
	mdpath, isMD = service.get_page_path(context, settings.wiki_path, safe_path)

	if not isMD:
		if os.path.isfile(mdpath) and not mdpath.endswith('.md'):
			safe_path = safe_path.replace('\\', '/')
			return send_from_directory(settings.wiki_path, safe_path)

	service.load_page(context, mdpath)
	if context.hasError():
		return render_template('error.html', header = head, data=context.error)
	return render_template('wiki.html',
												 header = head, content=service.html, metadata=service.metadata, path=path)

