

class MarkdownWriter:

	#----------------------------------
	def __init__(self):
		self.meta = {}
		self.tags = []
		self.body = ""

	#----------------------------------
	def add(self, name, value):
		self.meta[name] = value

	#----------------------------------
	def set_tags(self, list):
		self.tags = list

	#----------------------------------
	def add_tag(self, value):
		self.tags.append(value)

	#----------------------------------
	def save(self, filename):
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
