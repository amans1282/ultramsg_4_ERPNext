# Copyright (c) 2023, ERPGulf and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class Testwhatsappmessage(FrappeTestCase):
    """
    Test case for the whatsappmessage doctype.
    """

    def setUp(self):
        """
        Setup any state specific to the execution of the given module.
        This method is called before each test.
        """
        # Create a test record for whatsappmessage if necessary
        self.test_record = frappe.get_doc({
            'doctype': 'whatsappmessage',
            'title': 'Test Message',
            'message': 'This is a test message',
            'to_number': '1234567890',
            'time': frappe.utils.now()
        })
        self.test_record.insert()
    
    def tearDown(self):
        """
        Clean up any state that was set up during the test.
        This method is called after each test.
        """
        # Delete the test record
        if self.test_record:
            frappe.delete_doc('whatsappmessage', self.test_record.name)

    def test_whatsappmessage_creation(self):
        """
        Test the creation of a whatsappmessage record.
        """
        log_entry = frappe.get_doc('whatsappmessage', self.test_record.name)
        self.assertEqual(log_entry.title, 'Test Message')
        self.assertEqual(log_entry.message, 'This is a test message')
        self.assertEqual(log_entry.to_number, '1234567890')

    def test_whatsappmessage_validation(self):
        """
        Test the validation logic for a whatsappmessage record.
        """
        invalid_record = frappe.get_doc({
            'doctype': 'whatsappmessage',
            'title': '',
            'message': '',
            'to_number': '',
            'time': frappe.utils.now()
        })
        with self.assertRaises(frappe.ValidationError):
            invalid_record.insert()

    def test_whatsappmessage_deletion(self):
        """
        Test the deletion of a whatsappmessage record.
        """
        log_entry_name = self.test_record.name
        self.test_record.delete()
        self.assertIsNone(frappe.db.exists('whatsappmessage', log_entry_name))