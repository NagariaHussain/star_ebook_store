import frappe


def get_context(context):
	# --- OLD --- 
	# Leaving here for reference

	# context.ebooks = frappe.get_all(
	# 	"eBook",
	# 	fields=[
	# 		"name",
	# 		"cover_image",
	# 		"route",
	# 		"creation",
	# 		"author.full_name as author_name",
	# 	],
	# 	filters={"is_published": True},
	# 	order_by="creation desc"
	# )

	from frappe.query_builder.functions import Count

	EBook = frappe.qb.DocType("eBook")
	Author = frappe.qb.DocType("Author")
	EBookOrder = frappe.qb.DocType("eBook Order")

	query = (
		frappe.qb.from_(EBook)
		.left_join(Author)
		.on(Author.name == EBook.author)
		.left_join(EBookOrder)
		.on((EBookOrder.ebook == EBook.name) & (EBookOrder.status == "Paid"))
		.where(EBook.is_published == True)
		.groupby(EBook.name)
		.select(
			EBook.route,
			EBook.cover_image,
			EBook.name,
			Author.full_name.as_("author_name"),
			Count(EBookOrder.name).as_("sales_count"),
		)
		.orderby(EBook.creation)
	)

	context.ebooks = query.run(as_dict=True)