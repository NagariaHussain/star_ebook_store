import frappe
import razorpay

from frappe.utils.password import get_decrypted_password


@frappe.whitelist(allow_guest=True)
def create_ebook_order(ebook_name, customer_email):
	ebook_price_inr = frappe.db.get_value("eBook", ebook_name, "price_inr")
	order_data = {"amount": ebook_price_inr * 100, "currency": "INR"}  # convert to paisa

	key_id = frappe.db.get_single_value("Store Razorpay Settings", "key_id")
	key_secret = get_decrypted_password(
		"Store Razorpay Settings", "Store Razorpay Settings", "key_secret"
	)

	client = razorpay.Client(auth=(key_id, key_secret))
	razorpay_order = client.order.create(data=order_data)

	frappe.get_doc(
		{
			"doctype": "eBook Order",
			"ebook": ebook_name,
			"razorpay_order_id": razorpay_order["id"],
			"order_total": ebook_price_inr,
			"customer_email": customer_email,
		}
	).insert(ignore_permissions=True)

	return {
		"key_id": key_id,
		"order_id": razorpay_order["id"],
	}
