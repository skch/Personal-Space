import os
from flask import Blueprint, render_template, current_app, abort, send_from_directory
from services.content_parser import parse_markdown_file

wiki_bp = Blueprint('wiki', __name__)

@wiki_bp.route('/', defaults={'path': 'Home'})
@wiki_bp.route('/<path:path>')
def wiki_page(path):
	settings = current_app.config['SETTINGS']

	# Secure path traversal
	safe_path = os.path.normpath(path)
	if safe_path.startswith('..') or safe_path.startswith('/'):
		abort(404)

	full_path = os.path.join(settings.wiki_path, safe_path)

	# If the path explicitly has a non-markdown extension, serve it statically (e.g. images)
	if os.path.isfile(full_path) and not full_path.endswith('.md'):
		return send_from_directory(settings.wiki_path, safe_path)

	# Try resolving to a markdown file
	md_path = full_path + '.md' if not full_path.endswith('.md') else full_path

	if not os.path.exists(md_path):
		# Fallback to checking if it's a directory containing Home.md (github wiki style)
		if os.path.isdir(full_path):
			md_path = os.path.join(full_path, 'Home.md')
			if not os.path.exists(md_path):
				abort(404)
		else:
			abort(404)

	parsed = parse_markdown_file(md_path)
	if not parsed:
		abort(404)

	return render_template('wiki.html', content=parsed['html'], metadata=parsed['metadata'], path=path)
