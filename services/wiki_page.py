import json
import os
from common.rails_context import railway, RailsContext
from services.content_parser import parse_markdown_file
from services.markdown_reader import MarkdownReader
from services.markdown_writer import MarkdownWriter


class WikiPage:

# region Read Page
	# ==============================================
	@railway
	def get_page_path(self, context: RailsContext, wiki_path, safe_path):
		self.root_path = wiki_path
		# Secure path traversal
		if safe_path.startswith('..') or safe_path.startswith('/'):
			context.setError(False, f"Unsupported path: {safe_path}")
			return "", False

		full_path = os.path.join(wiki_path, safe_path)
		# If the path explicitly has a non-markdown extension, serve it statically (e.g. images)
		if os.path.isfile(full_path) and not full_path.endswith('.md'): return full_path, False
		return full_path, True

	# ==============================================
	@railway
	def load_page(self, context: RailsContext, full_path):
		md_path = self._validate_page_path(context, full_path)
		self._parse_page(context, md_path)
		return self._convert_page(context, md_path)

	#------------------------------------
	@railway
	def _validate_page_path(self, context, full_path):
		# Try resolving to a markdown file
		md_path = full_path + '.md' if not full_path.endswith('.md') else full_path

		if not os.path.exists(md_path):
			# Fallback to checking if it's a directory containing Home.md (github wiki style)
			if os.path.isdir(full_path):
				md_path = os.path.join(full_path, 'Home.md')
				if not os.path.exists(md_path):
					return context.setError(False, f"Home page not found: {md_path}")
			else:
				return context.setError(False, f"Page not found: {md_path}")
		return md_path

	#------------------------------------
	@railway
	def _parse_page(self, context, md_path):
		parsed = parse_markdown_file(md_path)
		if not parsed:
			return context.setError(False, f"Cannot parse page: {md_path}")
		self.html = parsed['html']
		self.metadata = parsed['metadata']
		self.markdown = parsed['raw_content']
		return True

	#------------------------------------
	@railway
	def _convert_page(self, context, md_path):
		reader = MarkdownReader()
		self.mdata = reader.convert(context, self.markdown)
		return True

# endregion

# region Save Page

	# ==============================================
	@railway
	def save_page(self, context: RailsContext, full_path, jbody):
		body = json.loads(jbody)
		md_path = self._validate_page_path(context, full_path)
		blocks = body['blocks']
		self._save_debug(blocks)
		self._save_json2md(context, blocks, md_path)
		return True

	#------------------------------------
	@railway
	def _save_json2md(self, context, blocks, md_path):
		newpath = md_path.replace('.md', '1.md')
		md = MarkdownWriter()
		for block in blocks:
			if block['type'] == 'paragraph':
				md.par(block['data']['text'])

		md.save(newpath)
		return True

# endregion


	#------------------------------------
	def _save_debug(self, data):
		text = json.dumps(data, ensure_ascii=False, indent=2)
		with open('_update.json', 'w') as f:
			f.write(text)


