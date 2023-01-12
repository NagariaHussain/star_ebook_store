# Copyright (c) 2022, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import cleanup_page_name


class eBook(WebsiteGenerator):
	def validate(self):
		if not self.route:
			self.route = f"store/{cleanup_page_name(self.name)}"

	def get_context(self, context):
		context.author = frappe.db.get_value(
			"Author", self.author, ["full_name as name", "bio"], as_dict=True
		)

		context.csrf_token = frappe.sessions.get_csrf_token()

	def send_via_email(self, recipient):
		author_name = frappe.db.get_value("Author", self.author, "full_name")
		args = {
			"name": self.name,
			"cover_image": self.cover_image,
			"author_name": author_name,
		}
		asset_attachments = [{"file_url": self.asset_file}]

		frappe.sendmail(
			[recipient],
			subject="[Star EBook Store] Your eBook has arrived!",
			attachments=asset_attachments,
			template="ebook_delivery",
			args=args,
		)
