# Copyright (c) 2022, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import cleanup_page_name


class eBook(WebsiteGenerator):
	def validate(self):
		if not self.route:
			self.route = f"/store/{cleanup_page_name(self.name)}"

	def get_context(self, context):
		context.author = frappe.db.get_value(
			"Author", self.author, ["full_name as name", "bio"], as_dict=True
		)
