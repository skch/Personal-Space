import os
from flask import Blueprint, render_template, current_app, abort, send_from_directory

from common.rails_context import RailsContext
from services.content_parser import parse_markdown_file
from services.wiki_page import WikiPage

wiki_bp = Blueprint('wiki', __name__)

@wiki_bp.route('/', defaults={'path': 'Home'})
@wiki_bp.route('/<path:path>')
def wiki_page(path):
	context = RailsContext()
	settings = current_app.config['SETTINGS']
	service = WikiPage()
	safe_path = os.path.normpath(path)
	mdpath, isMD = service.get_page_path(context, settings.wiki_path, safe_path)

	if not isMD:
		if os.path.isfile(mdpath) and not mdpath.endswith('.md'):
			return send_from_directory(settings.wiki_path, safe_path)

	service.load_page(context, mdpath)
	if context.hasError():
		return render_template('error.html', data=context.error)
	return render_template('wiki.html',
												 logo=settings.name, content=service.html, metadata=service.metadata, path=path)

