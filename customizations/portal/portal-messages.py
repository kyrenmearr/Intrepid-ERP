import frappe
from frappe import _


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/portal-messages"
		raise frappe.Redirect

	context.no_cache = 1
	context.title = _("Messages")

	# Messages sent by this user through the portal
	sent = frappe.get_all(
		"Communication",
		filters={
			"sender": frappe.session.user,
			"communication_type": "Communication",
			"communication_medium": "Portal",
		},
		fields=["name", "subject", "content", "communication_date", "sent_or_received", "sender_full_name"],
		order_by="communication_date desc",
		limit=100,
	)

	# Replies sent back to this user (sent_or_received=Sent, recipients contains user)
	replied = frappe.get_all(
		"Communication",
		filters={
			"recipients": frappe.session.user,
			"sent_or_received": "Sent",
			"communication_type": "Communication",
		},
		fields=["name", "subject", "content", "communication_date", "sent_or_received", "sender_full_name"],
		order_by="communication_date desc",
		limit=100,
	)

	all_messages = sent + replied
	all_messages.sort(key=lambda x: str(x.get("communication_date") or ""), reverse=True)
	context.messages = all_messages


@frappe.whitelist()
def send_message(subject, content):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in to send a message."))

	full_name = frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user

	comm = frappe.new_doc("Communication")
	comm.communication_type = "Communication"
	comm.communication_medium = "Portal"
	comm.sent_or_received = "Received"
	comm.sender = frappe.session.user
	comm.sender_full_name = full_name
	comm.subject = subject or _("Message from Portal")
	comm.content = content
	comm.insert(ignore_permissions=True)
	frappe.db.commit()
	return comm.name
