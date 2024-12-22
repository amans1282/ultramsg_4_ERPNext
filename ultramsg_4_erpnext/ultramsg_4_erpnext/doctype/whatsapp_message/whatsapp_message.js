// Copyright (c) 2023, ERPGulf and contributors
// For license information, please see license.txt

frappe.ui.form.on("whatsapp message", {
    refresh: function(frm) {
        // Add a custom button to send a test message
        frm.add_custom_button(__("Send Test Message"), function() {
            // Validate required fields
            if (!frm.doc.token || !frm.doc.to || !frm.doc.message_url) {
                frappe.msgprint(__("Please fill in the required fields: Token, Recipient, and Message URL."));
                return;
            }
            
            // Call the server-side method to send the message
            frm.call("msg", {
                token: frm.doc.token,
                recipient: frm.doc.to,
                message_url: frm.doc.message_url,
            }).then(response => {
                // Display the server response
                if (response.message) {
                    frappe.msgprint(response.message);
                } else {
                    frappe.msgprint(__("No response from server."));
                }
            }).catch(error => {
                // Handle any errors
                frappe.msgprint(__("An error occurred while sending the message. Please try again."));
                console.error(error);
            });
        }, __("Send Test Message"));
    }
});