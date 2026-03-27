import os
from flask import Blueprint, render_template, current_app, abort, send_from_directory
from markupsafe import Markup

from common.rails_context import RailsContext
from services.content_parser import parse_markdown_file
from services.page_tools import get_header
from services.wiki_page import WikiPage

wiki_bp = Blueprint('wiki', __name__)


@wiki_bp.route('/edit/<path:path>', methods=['GET'])
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

	service.load_page(context, mdpath)
	mdata = Markup(service.mdata)
	if context.hasError():
		return render_template('error.html', header = head, data=context.error)
	return render_template('wiki_edit.html',
												 header = head, raw_content=mdata, metadata=service.metadata, path=path)




@wiki_bp.route('/save/<path:path>', methods=['POST'])
def wiki_save(path):
	wiki_folder = current_app.config['WIKI_FOLDER']
	safe_path = os.path.normpath(path)
	if safe_path.startswith('..') or safe_path.startswith('/'):
		abort(404)

	full_path = os.path.join(wiki_folder, safe_path)
	md_path = full_path + '.md' if not full_path.endswith('.md') else full_path

	os.makedirs(os.path.dirname(md_path), exist_ok=True)

	data = request.get_json()
	if not data or 'content' not in data:
		return jsonify({'error': 'No content provided'}), 400

	with open(md_path, 'w', encoding='utf-8') as f:
		f.write(data['content'])

	return jsonify({'success': True})



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

