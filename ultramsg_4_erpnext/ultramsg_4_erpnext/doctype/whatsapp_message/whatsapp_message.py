# Copyright (c) 2023, ERPGulf and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class whatsappmessage(Document):
    @frappe.whitelist()
    def msg(self, token, recipient, message_url):
        """
        Sends a WhatsApp message using the provided token, recipient, and message URL.
        
        Args:
            token (str): The authentication token for the WhatsApp API.
            recipient (str): The phone number of the message recipient.
            message_url (str): The URL of the WhatsApp API endpoint.
        
        Returns:
            str: The response text from the WhatsApp API or an error message.
        """
        payload = {
            'token': token,
            'to': recipient,
            'body': "This message is for testing",
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(message_url, data=payload, headers=headers)
            return response.text
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), 'WhatsApp Message Error')
            return str(e)