import os
import glob
from services.content_parser import parse_markdown_file
from common.rails_context import railway, RailsContext
from collections import defaultdict

class PeopleService:

	#==============================================
	@railway
	def load_contacts(self, context: RailsContext, path: str):
		if not os.path.exists(path):
			return context.setError({}, f"Contacts folder does not exist: {path}")

		self.base_path = path
		self.contacts = {}
		people = os.listdir(path)
		for pfolder in people:
			contact = self._read_contact(context, pfolder)
			if contact:	self.contacts[pfolder] = contact
		return True

	#==============================================
	@railway
	def get_by_group(self, context):
		grouped_contacts = defaultdict(list)
		for cid, contact in self.contacts.items():
			grouped_contacts[contact.get('team')].append(contact)
		return grouped_contacts

	#------------------------------------
	@railway
	def _read_contact(self, context, pfolder):
		contact_path = os.path.join(self.base_path, pfolder)
		if not os.path.isdir(contact_path): return False
		md_files = glob.glob(os.path.join(contact_path, '*.md'))
		img_files = (glob.glob(os.path.join(contact_path, '*.jpg')) +
								 glob.glob(os.path.join(contact_path, '*.png')) +
								 glob.glob(os.path.join(contact_path, '*.jpeg')))

		if not md_files: return False
		parsed = parse_markdown_file(md_files[0])
		if not parsed: return context.setError(False, f"Failed to parse {pfolder}")
		meta = parsed['metadata']
		meta['id'] = pfolder
		meta['FullName'] = f"{meta.get('FirstName', '')} {meta.get('LastName', '')}"
		meta['image'] = os.path.basename(img_files[0]) if img_files else None
		meta['html'] = parsed['html']
		return meta

	#==============================================
	@railway
	def get_by_id(self, context, contact_id):
		return self.contacts.get(contact_id)
