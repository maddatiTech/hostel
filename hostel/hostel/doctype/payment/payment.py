# Copyright (c) 2022, milan thapa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Payment(Document):
    def after_insert(self):
        try:
            fee_cat_list = ["Monthly Fee", "Admission Fee", "Security Deposit"]
            if self.pmt_fee_cat in fee_cat_list:
                frappe.db.set_value('Fee Management', {
                                    "std_name": self.pmt_std}, 'std_rem_bal', self.pmt_rem_balance-self.pmt_amt)
                frappe.msgprint("Fee Updated.")
                return
            if self.pmt_fee_cat == "Fine":
                frappe.db.set_value('Fee Management', {
                                    "std_name": self.pmt_std}, 'std_fine_amt', self.pmt_rem_fine-self.pmt_amt)
                frappe.msgprint("Fee Updated.")
                return
            if self.pmt_fee_cat == "Extras":
                frappe.db.set_value('Fee Management', {
                                    "std_name": self.pmt_std}, 'std_extras', self.pmt_extra_amt-self.pmt_amt)
                frappe.msgprint("Fee Updated.")
        except:
            frappe.throw("Error while updating fees.")
