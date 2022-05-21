import frappe
import datetime
from frappe.utils import getdate, date_diff, add_to_date


def auto_fee_mgmt():
    for student in frappe.db.get_list('Students', filters={'std_status': 'Active'}, fields=["name", "std_branch_name", "std_room_number", "std_month_fee"]):
        for fee in frappe.db.get_list('Fee Management', filters={"std_name": student.name}, fields=["name", "std_rem_bal", "std_fee_update"]):
            if(frappe.db.exists({"doctype": "Fee Management", "std_name": student.name})):
                if((date_diff(getdate(), fee.std_fee_update) >= 30)):
                    print(fee,date_diff(getdate(), fee.std_fee_update))
                    after_30_days = add_to_date(fee.std_fee_update,days=30,as_datetime=True)
                    frappe.db.set_value('Fee Management', {
                        "std_name": student.name}, {
                            "std_branch": student.std_branch_name,
                            "std_room_num": student.std_room_number,
                            "std_fee_update": after_30_days,
                            "std_rem_bal": fee.std_rem_bal+student.std_month_fee})
                    frappe.reload_doctype("Fee Management")
                    print('Auto fee management updated')
            else:
                frappe.throw("Record doesnt exists for auto fee management")
