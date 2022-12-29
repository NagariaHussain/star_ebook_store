import frappe


def get_context(context):
	context.ebooks = frappe.get_all(
		"eBook",
		fields=[
			"name",
			"cover_image",
			"price_inr",
			"format",
			"route",
			"creation",
			"author.full_name as author_name",
		],
		filters={"is_published": True},
		order_by="creation desc"
	)
