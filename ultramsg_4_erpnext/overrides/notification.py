import frappe
import requests
from frappe.model.document import Document

class ERPGulfNotification(Notification):
    # Create PDF and return as base64 encoded URL
    def create_pdf(self, doc):
        file = frappe.get_print(doc.doctype, doc.name, self.print_format, as_pdf=True)
        pdf_bytes = io.BytesIO(file)
        pdf_base64 = base64.b64encode(pdf_bytes.getvalue()).decode()
        in_memory_url = f"data:application/pdf;base64,{pdf_base64}"
        return in_memory_url

    # Send WhatsApp message with PDF
    @frappe.whitelist()
    def send_whatsapp_with_pdf(self, doc, context):
        memory_url = self.create_pdf(doc)
        whatsapp_config = frappe.get_doc('WhatsApp Message', 'your-config-name')
        token = whatsapp_config.token
        api_base_url = whatsapp_config.api_base_url
        vendor_uid = whatsapp_config.vendor_uid
        from_phone_number_id = whatsapp_config.from_phone_number_id
        template_name = whatsapp_config.template_name
        template_language = whatsapp_config.template_language

        msg1 = frappe.render_template(self.message, context)
        recipients = self.get_receiver_list(doc, context)
        
        if not token or not recipients or not api_base_url or not vendor_uid:
            frappe.log_error("Missing token, recipients, API base URL, or vendor UID", "WhatsApp Notification Error")
            return

        for recipient in recipients:
            message_url = f"{api_base_url}/{vendor_uid}/contact/send-template-message"
            payload = {
                "from_phone_number_id": from_phone_number_id,
                "phone_number": recipient,
                "template_name": template_name,
                "template_language": template_language,
                "header_document": memory_url,
                "header_document_name": doc.full_name,
                "header_field_1": doc.full_name,
                "field_1": doc.age,
                "field_2": doc.full_name,
                "field_3": doc.first_name,
                "field_4": doc.last_name,
                "button_0": doc.email,
                "button_1": doc.phone_number,
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            try:
                time.sleep(10)
                response = requests.post(message_url, json=payload, headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get("sent") == "true":
                        current_time = now()
                        frappe.get_doc({
                            "doctype": "ultramsg_4_ERPNext log",
                            "title": "Whatsapp message and PDF successfully sent",
                            "message": msg1,
                            "to_number": doc.custom_mobile_phone,
                            "time": current_time
                        }).insert()
                    else:
                        frappe.log_error(response_json.get("error"), "WhatsApp API Error")
                else:
                    frappe.log_error(f"HTTP Error: {response.status_code}", "WhatsApp API Error")
            except Exception as e:
                frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())

    # Send WhatsApp message without PDF
    def send_whatsapp_without_pdf(self, doc, context):
        whatsapp_config = frappe.get_doc('WhatsApp Message', 'your-config-name')
        token = whatsapp_config.token
        api_base_url = whatsapp_config.api_base_url
        vendor_uid = whatsapp_config.vendor_uid
        from_phone_number_id = whatsapp_config.from_phone_number_id
        template_name = whatsapp_config.template_name
        template_language = whatsapp_config.template_language

        msg1 = frappe.render_template(self.message, context)
        recipients = self.get_receiver_list(doc, context)
        
        if not token or not recipients or not api_base_url or not vendor_uid:
            frappe.log_error("Missing token, recipients, API base URL, or vendor UID", "WhatsApp Notification Error")
            return

        for recipient in recipients:
            message_url = f"{api_base_url}/{vendor_uid}/contact/send-template-message"
            payload = {
                "from_phone_number_id": from_phone_number_id,
                "phone_number": recipient,
                "template_name": template_name,
                "template_language": template_language,
                "header_field_1": doc.full_name,
                "field_1": doc.age,
                "field_2": doc.full_name,
                "field_3": doc.first_name,
                "field_4": doc.last_name,
                "button_0": doc.email,
                "button_1": doc.phone_number,
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            try:
                time.sleep(10)
                response = requests.post(message_url, json=payload, headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get("sent") == "true":
                        current_time = now()
                        frappe.get_doc({
                            "doctype": "ultramsg_4_ERPNext log",
                            "title": "Whatsapp message successfully sent",
                            "message": msg1,
                            "to_number": doc.custom_mobile_phone,
                            "time": current_time
                        }).insert()
                    else:
                        frappe.log_error(response_json.get("error"), "WhatsApp API Error")
                else:
                    frappe.log_error(f"HTTP Error: {response.status_code}", "WhatsApp API Error")
                return response.text
            except Exception as e:
                frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())

    # Main send function that decides to send with or without PDF
    def send(self, doc):
        context = {"doc": doc, "alert": self, "comments": None}
        if doc.get("_comments"):
            context["comments"] = json.loads(doc.get("_comments"))
        if self.is_standard:
            self.load_standard_properties(context)
        try:
            if self.channel == "whatsapp message":
                if self.attach_print or self.print_format:
                    frappe.enqueue(
                        self.send_whatsapp_with_pdf(doc, context),
                        queue="short",
                        timeout=200,
                        doc=doc,
                        context=context
                    )
                else:
                    frappe.enqueue(
                        self.send_whatsapp_without_pdf(doc, context),
                        queue="short",
                        timeout=200,
                        doc=doc,
                        context=context
                    )
        except Exception as e:
            frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())
        super(ERPGulfNotification, self).send(doc)

    # Get the list of receivers based on document field and role
    def get_receiver_list(self, doc, context):
        receiver_list = []
        for recipient in self.recipients:
            if recipient.condition:
                if not frappe.safe_eval(recipient.condition, None, context):
                    continue
            if recipient.receiver_by_document_field:
                fields = recipient.receiver_by_document_field.split(",")
                if len(fields) > 1:
                    for d in doc.get(fields[1]):
                        phone_number = d.get(fields[0])
                        if phone_number:
                            receiver_list.append(phone_number)
            if recipient.receiver_by_document_field == "owner":
                receiver_list += get_user_info([dict(user_name=doc.get("owner"))], "mobile_no")
            elif recipient.receiver_by_document_field:
                receiver_list.append(doc.get(recipient.receiver_by_document_field))
            if recipient.receiver_by_role:
                receiver_list += get_info_based_on_role(recipient.receiver_by_role, "mobile_no")
        
        # Remove duplicates and None values
        receiver_list = list(set(receiver_list))
        final_receiver_list = [item for item in receiver_list if item is not None]
        return final_receiver_list