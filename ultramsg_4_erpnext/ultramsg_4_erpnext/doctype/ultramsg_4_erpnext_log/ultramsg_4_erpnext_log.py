# Copyright (c) 2023, ERPGulf and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ultramsg_4_ERPNextlog(Document):
    """
    This class represents the ultramsg_4_ERPNextlog document in ERPNext.
    It is used to log messages sent via UltraMsg integration with ERPNext.
    """
    def before_save(self):
        """
        This method is called before the document is saved.
        You can add custom validations or modifications here.
        """
        self.validate_fields()

    def validate_fields(self):
        """
        Custom validation logic for the document fields.
        """
        if not self.title:
            frappe.throw("Title is required")
        if not self.to_number:
            frappe.throw("To Number is required")
        if not self.message:
            frappe.throw("Message is required")

    def after_insert(self):
        """
        This method is called after the document is inserted.
        You can add custom post-insert logic here.
        """
        frappe.msgprint(f"Log entry '{self.title}' created successfully.")