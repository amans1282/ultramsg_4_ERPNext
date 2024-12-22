import frappe
frappe.init(site="newsite.erpgulf.com")
frappe.connect()
subject = frappe.db.get_value("Notification", "aysha", "subject")
print(subject)
print(frappe.session.user)
data = frappe.db.get_list('Employee')
