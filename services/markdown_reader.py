from common.rails_context import railway, RailsContext
import json
import re
import time
import string
import random


MAGIC_WORD = "⩀"

class MarkdownReader:

	#------------------------------------
	@railway
	def convert(self, context: RailsContext, markdown):
		data = self.parse_markdown_to_editorjs(markdown)
		self.save_data_debug(data['blocks'])
		text = json.dumps(data['blocks'], ensure_ascii=False)
		return text.replace(MAGIC_WORD,"\\'")

	#------------------------------------
	def generate_id(self, length=10):
		chars = string.ascii_letters + string.digits
		return ''.join(random.choice(chars) for _ in range(length))

	def process_inline_elements(self, text: str) -> str:
		text = re.sub(r'(?<!\!)\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
		text = re.sub(r'`(.*?)`', r'<code class="inline-code">\1</code>', text)
		return text.replace('"', MAGIC_WORD)

	#------------------------------------
	def parse_markdown_to_editorjs(self, markdown_text: str) -> dict:
		blocks = []

		# Split text by blank lines to get basic blocks
		raw_blocks = re.split(r'\n\s*\n', markdown_text.strip())

		for raw_block in raw_blocks:
			raw_block = raw_block.strip()
			if not raw_block:	continue

			# Check for headers: # Header
			header_match = re.match(r'^(#{1,6})\s+(.*)$', raw_block, flags=re.MULTILINE)
			if header_match:
				level = len(header_match.group(1))
				text = self.process_inline_elements(header_match.group(2))
				blocks.append({
					"id": self.generate_id(),
					"type": "header",
					"data": {
						"text": text,
						"level": level
					}
				})
				continue

			# Check for delimiter: ---, ***, ___
			if re.match(r'^(\*\*\*|---|___)$', raw_block):
				blocks.append({
					"id": self.generate_id(),
					"type": "delimiter",
					"data": {}
				})
				continue

			# Check for image: ![caption](url)
			img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', raw_block)
			if img_match:
				caption = img_match.group(1)
				url = img_match.group(2)
				blocks.append({
					"id": self.generate_id(),
					"type": "image",
					"data": {
						"url": url,
						"caption": caption,
						"withBorder": False,
						"withBackground": False,
						"stretched": False
					}
				})
				continue

			# Check for list
			lines = raw_block.split('\n')
			is_list = all(re.match(r'^[\*\-\+]\s+.*$|^\d+\.\s+.*$', line.strip()) for line in lines)
			if len(lines) > 0 and is_list:
				style = "unordered"
				if re.match(r'^\d+\.', lines[0].strip()):
					style = "ordered"

				items = []
				for line in lines:
					content = re.sub(r'^[\*\-\+]\s+|^\d+\.\s+', '', line.strip())
					content = self.process_inline_elements(content)
					items.append({
						"content": content,
						"meta": {},
						"items": []
					})

				blocks.append({
					"id": self.generate_id(),
					"type": "list",
					"data": {
						"style": style,
						"meta": {},
						"items": items
					}
				})
				continue

			# Check for table
			if len(lines) >= 1 and all('|' in line for line in lines):
				content = []
				with_headings = False
				for line in lines:
					# Ignore table separator like |---|---|
					if re.match(r'^\|?[\s\-:]+\|?(\s*\|[\s\-:]+)*\|?$', line):
						with_headings = True
						continue
					row = [self.process_inline_elements(cell.strip()) for cell in line.strip().strip('|').split('|')]
					content.append(row)

				blocks.append({
					"id": self.generate_id(),
					"type": "table",
					"data": {
						"withHeadings": with_headings,
						"stretched": False,
						"content": content
					}
				})
				continue

			# Default to paragraph
			# We can keep inline HTML like <mark> or <a href="..."> intact as Editor.js handles them.
			text = self.process_inline_elements(raw_block.replace('\n', ' '))
			blocks.append({
				"id": self.generate_id(),
				"type": "paragraph",
				"data": {
					"text": text
				}
			})

		return {
			"time": int(time.time() * 1000),
			"blocks": blocks,
			"version": "2.31.5"
		}


	def save_data_debug(self, data):
		text = json.dumps(data, ensure_ascii=False, indent=2)
		text = text.replace(MAGIC_WORD, "\\'")
		with open('_blocks.json', 'w') as f:
			f.write(text)

