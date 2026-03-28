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
	def save_page(self, context: RailsContext, full_path, mbody):

		md_path = self._validate_page_path(context, full_path)
		self._save_md(context, mbody, md_path)
		return True

	#------------------------------------
	@railway
	def _save_md(self, context, mdtext, md_path):
		try:
			with open(md_path, 'w') as file: file.write(mdtext)
			return True
		except OSError as e:
			print(f"Error saving file {md_path}: {e}")
			return False


	# ==============================================
	@railway
	def save_block_page(self, context: RailsContext, full_path, jbody):
		body = json.loads(jbody)
		md_path = self._validate_page_path(context, full_path)
		blocks = body['blocks']
		self._save_debug(blocks)
		self._save_json2md(context, blocks, md_path)
		return True

	#------------------------------------
	@railway
	def _save_json2md(self, context, blocks, md_path):
		#newpath = md_path.replace('.md', '1.md')
		newpath = md_path
		md = MarkdownWriter()
		for block in blocks:
			type = block['type']
			data = block['data']
			match type:
				case 'header': md.header(data['level'], data['text'])
				case 'code': md.code(data['code'])
				case 'delimiter': md.hline()
				case 'quote': self._print_quote(md, data)
				case 'list': self._print_list(md, data)
				case 'table': self._print_table(md, data)
				case 'image': self._print_image(md, data)
				case 'warning': self._print_warning(md, data)
				case _: md.par(data['text'])


		md.save(newpath)
		return True

	#------------------------------------
	def _print_quote(self, md, data):
		text = data['text']
		author = data['caption']
		#aligh = data['alignment']
		md.quote(text, author)
		md.line('')

	#------------------------------------
	def _print_list(self, md, data):
		cnt = 1
		match data['style']:
			case 'ordered':
				for item in data['items']:
					md.numbered(cnt, item['content'])
					cnt += 1
			case 'unordered':
				for item in data['items']: md.bullet(item['content'])
			case 'checklist':
				for item in data['items']: md.todoitem(item['content'], item['meta']['checked'])
		md.line('')

	#------------------------------------
	def _print_table(self, md, data):
		first = True
		rows = data['content']
		for row in rows:
			if first:
				md.tableHeader(row)
				first = False
			else:
				for i in range(len(row)):
					md.tableColumn(row[i], i == len(row) - 1)
		md.line('')

	#------------------------------------
	def _print_image(self, md, data):
		url = data['url']
		caption = data['caption']
		#withBorder = data['withBorder']
		md.image(url, caption)
		md.line('')

	#------------------------------------
	def _print_warning(self, md, data):

		title = data['title']
		message = data['message']
		md.line('')

# endregion


	#------------------------------------
	def _save_debug(self, data):
		text = json.dumps(data, ensure_ascii=False, indent=2)
		with open('_update.json', 'w') as f:
			f.write(text)



