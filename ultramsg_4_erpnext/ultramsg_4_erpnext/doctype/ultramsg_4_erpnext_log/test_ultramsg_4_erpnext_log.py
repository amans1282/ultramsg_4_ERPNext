# Copyright (c) 2023, ERPGulf and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class Testultramsg_4_ERPNextlog(FrappeTestCase):
    """
    Test case for the ultramsg_4_ERPNextlog doctype
    """

    def setUp(self):
        """
        Setup any state specific to the execution of the given module.
        This method is called before each test.
        """
        # Create a test record for ultramsg_4_ERPNextlog if necessary
        self.test_record = frappe.get_doc({
            'doctype': 'ultramsg_4_ERPNextlog',
            'title': 'Test Log Entry',
            'message': 'This is a test log entry',
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
            self.test_record.delete()

    def test_log_entry_creation(self):
        """
        Test the creation of a log entry
        """
        log_entry = frappe.get_doc('ultramsg_4_ERPNextlog', self.test_record.name)
        self.assertEqual(log_entry.title, 'Test Log Entry')
        self.assertEqual(log_entry.message, 'This is a test log entry')
        self.assertEqual(log_entry.to_number, '1234567890')

    def test_log_entry_deletion(self):
        """
        Test the deletion of a log entry
        """
        log_entry_name = self.test_record.name
        self.test_record.delete()
        self.assertIsNone(frappe.db.exists('ultramsg_4_ERPNextlog', log_entry_name))