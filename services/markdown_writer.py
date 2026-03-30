

class MarkdownWriter:

	#----------------------------------
	def __init__(self):
		self.mdtext = ""
		self.metadata = {}
		self.tags = []


	#----------------------------------
	def set_tags(self, list):
		self.tags = list

	#----------------------------------
	def add_tag(self, value):
		self.tags.append(value)


	#----------------------------------
	def save_old(self, filename):
		text = '---\n'
		for key, value in self.meta.items():
			if isinstance(value, list):
				text += f'{key}:\n'
				for item in value:
					text += f'  - {item}\n'
			else:
				text += f'{key}: {value}\n'
		if self.tags:
			text += 'tags:\n'
			for tag in self.tags:
				text += f'  - {tag}\n'
		text += '---\n\n'
		text += self.body
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(text)



	# ==============================================
	def setValue(self, name, value):
		self.metadata[name] = value

	# ==============================================
	def addMetadata(self, meta):
		self.metadata.update(meta)

	# ==============================================
	def addValue(self, name, value):
		if name in self.metadata:
			list = self.metadata[name]
			list.append(value)
		else:
			list = [value]
		self.metadata[name] = list

	# ==============================================
	def header(self, level, text):
		line = '#' * level
		line = line + " " + text
		self.mdtext += line + "\n\n"

	# ==============================================
	def code(self, text, lang=""):
		self.mdtext += f"```{lang}\n"
		self.mdtext += text + "\n"
		self.mdtext += "```\n\n"

	# ==============================================
	def mermaid(self, text):
		self.mdtext += "```mermaid\n"
		self.mdtext += text + "\n"
		self.mdtext += "```\n\n"

	# ==============================================
	def jsontext(self, text):
		self.mdtext += "```json\n"
		self.mdtext += text + "\n"
		self.mdtext += "```\n\n"

	# ==============================================
	def par(self, text = ""):
		self.mdtext = self.mdtext + text + "\n\n"

	# ==============================================
	def quote(self, text, author = ""):
		self.mdtext = self.mdtext + f"> {text}\n"
		if author:
				self.mdtext = self.mdtext + f"*{author}*\n"
		self.mdtext = self.mdtext + "\n"

	# ==============================================
	def line(self, text = ""):
		self.mdtext = self.mdtext + text + "\n"

	# ==============================================
	def image(self, url, caption):
		self.mdtext = self.mdtext +f"![{caption}]({url})\n\n"

	# ==============================================
	def list(self, id, text):
		self.mdtext = self.mdtext + f"{id}. " + text + "\n"

	# ==============================================
	def bullet(self, text):
		self.mdtext = self.mdtext + "* " + text + "\n"

	# ==============================================
	def bullet2(self, text):
		self.mdtext = self.mdtext + "   * " + text + "\n"

	# ==============================================
	def bullet3(self, text):
		self.mdtext = self.mdtext + "      * " + text + "\n"

	# ==============================================
	def numbered(self, num: int, text):
		self.mdtext = self.mdtext + f"{num}. {text}\n"

	# ==============================================
	def todoitem(self,  text, checked = False):
		if checked:
			self.mdtext = self.mdtext + f"- [x] {text}\n"
		else:
			self.mdtext = self.mdtext + f"- [ ] {text}\n"

	# ==============================================
	def hline(self):
		self.mdtext = self.mdtext + "---\n\n"

	# ==============================================
	def tableHeader(self, header, align = None):
		self.mdtext += "\n"
		self.mdtext += "| "
		for col in header:
			self.mdtext += f"{col} | "
		self.mdtext += "\n| "

		for cnt, col in enumerate(header):
			ca = align[cnt] if align else 'L'
			hl = self._create_table_divider(ca)
			self.mdtext += f"{hl} | "
		self.mdtext += "\n"

	# -----------------------------------
	def _create_table_divider(self, ca):
		if ca == 'C':
			return ':----------:'
		elif ca == 'R':
			return '----------:'
		else:
			return '----------'

	# ==============================================
	def tableColumn(self, value, last=False):
		self.mdtext += f"| {value} "
		if last:
			self.mdtext += " |\n"

	# ==============================================
	def footer(self):
		self.mdtext += "\n---\nThis page was automatically generated from data 🌀\n"

	# ==============================================
	def save(self, fname):
		try:
			if self.metadata:
				text = "---\n"
				for key, value in self.metadata.items():
					text += self._append_meta_value(key, value)
				#text += yaml.dump(self.metadata, sort_keys=False)
				text += f"---\n{self.mdtext}"
			else:
				text = self.mdtext
			with open(fname, 'w', encoding="utf-8") as file: file.write(text)
			return True
		except OSError as e:
			print(f"Error saving file {fname}: {e}")
			return False

	#----------------------------------
	def _append_meta_value(self, key, value):
		text = f"{key}:"
		if isinstance(value, str):
			text += f' "{value}"\n'
		if isinstance(value, int):
			text += f' {value}\n'
		if isinstance(value, float):
			text += f' {value}\n'
		if isinstance(value, list):
			text += "\n"
			for item in value:
				text += f"  - {item}\n"
		return text

