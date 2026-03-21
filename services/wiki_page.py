import os
from common.rails_context import railway, RailsContext
from services.content_parser import parse_markdown_file

class WikiPage:

	# ==============================================
	@railway
	def get_page_path(self, context: RailsContext, wiki_path, safe_path):
		self.root_path = wiki_path
		# Secure path traversal
		if safe_path.startswith('..') or safe_path.startswith('/'):
			return context.setError(False, f"Unsupported path: {safe_path}")

		full_path = os.path.join(wiki_path, safe_path)
		# If the path explicitly has a non-markdown extension, serve it statically (e.g. images)
		if os.path.isfile(full_path) and not full_path.endswith('.md'): return False
		return full_path

	# ==============================================
	@railway
	def load_page(self, context: RailsContext, full_path):
		md_path = self._validate_page_path(context, full_path)
		return self._parse_page(context, md_path)

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
		return True
