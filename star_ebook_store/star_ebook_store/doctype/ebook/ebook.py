# Copyright (c) 2022, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe

from frappe.website.website_generator import WebsiteGenerator


class eBook(WebsiteGenerator):
	def get_context(self, context):
		context.author = frappe.db.get_value(
			"Author", self.author, ["full_name as name", "bio"], as_dict=True
		)
