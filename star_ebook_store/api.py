import frappe
import razorpay

from frappe.utils.password import get_decrypted_password

def get_razorpay_client():
	key_id = frappe.db.get_single_value("Store Razorpay Settings", "key_id")
	key_secret = get_decrypted_password(
		"Store Razorpay Settings", "Store Razorpay Settings", "key_secret"
	)

	return razorpay.Client(auth=(key_id, key_secret))

@frappe.whitelist(allow_guest=True)
def create_ebook_order(ebook_name):
	ebook_price_inr = frappe.db.get_value("eBook", ebook_name, "price_inr")
	order_data = {"amount": ebook_price_inr * 100, "currency": "INR"}  # convert to paisa

	client = get_razorpay_client()
	razorpay_order = client.order.create(data=order_data)

	frappe.get_doc(
		{
			"doctype": "eBook Order",
			"ebook": ebook_name,
			"razorpay_order_id": razorpay_order["id"],
			"order_amount": ebook_price_inr,
		}
	).insert(ignore_permissions=True)

	return {
		"key_id": client.auth[0],
		"order_id": razorpay_order["id"],
	}


@frappe.whitelist(allow_guest=True)
def handle_razorpay_webhook():
	form_dict = frappe.local.form_dict

	payload = frappe.request.get_data()

	verify_webhook_signature(payload)  # for security purposes

	# Get payment details
	payment_entity = form_dict["payload"]["payment"]["entity"]
	razorpay_order_id = payment_entity["order_id"]
	razorpay_payment_id = payment_entity["id"]
	customer_email = payment_entity["email"]
	event = form_dict.get("event")

	# Process the order
	ebook_order = frappe.get_doc("eBook Order", {"razorpay_order_id": razorpay_order_id})
	if event in ("order.paid", "payment.captured") and ebook_order.status != "Paid":
		ebook_order.update(
			{
				"razorpay_payment_id": razorpay_payment_id,
				"status": "Paid",
				"customer_email": customer_email,
			}
		)
		ebook_order.save(ignore_permissions=True)


def verify_webhook_signature(payload):
	signature = frappe.get_request_header("X-Razorpay-Signature")
	webhook_secret = get_decrypted_password(
		"Store Razorpay Settings", "Store Razorpay Settings", "webhook_secret"
	)

	client = get_razorpay_client()
	client.utility.verify_webhook_signature(payload.decode(), signature, webhook_secret)
