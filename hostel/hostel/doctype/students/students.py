# Copyright (c) 2022, milan thapa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Students(Document):
    def validate(self):
        if not frappe.db.exists("Students",self.name):
            frappe.msgprint('New document created')
            room_details = frappe.get_doc('Branch', self.std_branch_name).as_dict()
            req_room = [x for x in room_details['room_details']if x['room_number'] == int(self.std_room_number)]
            bed_occupied = req_room[0]['room_bed_occupied']
            bed_capacity = req_room[0]['room_bed_capacity']
            if(bed_capacity == bed_occupied):
                frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'bed_availability', "No")
                frappe.db.commit()
                frappe.throw("Bed Not Available")
            elif((bed_capacity - bed_occupied) == 1):
                frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied+1)
                frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'bed_availability', "No")
                frappe.db.commit()
                frappe.msgprint('New Student Added To The Room')
            else:
                frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied+1)
                frappe.db.commit()
                frappe.msgprint('New Student Added To The Room')
        else:
            frappe.msgprint('Details Updated')
            prev_status = frappe.db.get_value('Students', self.name, 'std_status')
            curr_status = self.std_status
            if(prev_status != curr_status and curr_status == 'Active'):
                room_details = frappe.get_doc('Branch', self.std_branch_name).as_dict()
                req_room = [x for x in room_details['room_details']if x['room_number'] == self.std_room_number]
                bed_occupied = int(req_room[0]['room_bed_occupied'])
                bed_capacity = int(req_room[0]['room_bed_capacity'])
                if(bed_capacity == bed_occupied):
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'bed_availability', "No")
                    frappe.db.commit()
                    frappe.throw("Bed Not Available")
                elif((bed_capacity - bed_occupied) == 1):
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied+1)
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'bed_availability', "No")
                    frappe.db.commit()
                    frappe.msgprint('Student Room Reassigned')
                else:
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied+1)
                    frappe.db.commit()
                    frappe.msgprint('Student Room Reassigned')
            elif(prev_status != curr_status and curr_status == 'Left'):
                room_details = frappe.get_doc('Branch', self.std_branch_name).as_dict()
                req_room = [x for x in room_details['room_details']if x['room_number'] == self.std_room_number]
                bed_occupied = int(req_room[0]['room_bed_occupied'])
                bed_capacity = int(req_room[0]['room_bed_capacity'])
                if(bed_capacity == bed_occupied):
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied-1)
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'bed_availability', "Yes")
                    frappe.db.commit()
                    frappe.msgprint('Student left the room')
                else:
                    frappe.db.set_value('Rooms', {'parent': self.std_branch_name, 'room_number': self.std_room_number}, 'room_bed_occupied', bed_occupied-1)
                    frappe.db.commit()
                    frappe.msgprint('Student left the room')

    def after_insert(self):
        try:
            doc = frappe.get_doc({
                'doctype': 'Fee Management',
                'std_name': self.name,
                'std_branch': self.std_branch_name,
                'std_room_num': self.std_room_number,
                'std_fee_update': self.std_joined_date,
                'std_rem_bal': self.std_month_fee+self.std_admission_fee+self.std_security_deposit
            })
            doc.insert()
            frappe.db.commit()
            frappe.msgprint("New payment entries created.")
        except:
            frappe.throw("Error while generating payment entries")
