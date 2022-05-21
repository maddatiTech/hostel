// Copyright (c) 2022, milan thapa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Students", {
  onload: function (frm) {
    frm.set_value('room_avail_status', 0)
    frm.refresh_field("room_avail_status")
    frm.refresh_field("std_room_details")
    frm.set_intro(
      "Welcome to " + " " + frm.doc.name + " " + "Document",
      "blue"
    );
  },
  std_branch_name: function (frm) {
    if (frm.doc.std_branch_name) {
      frm.clear_table("std_room_details");
      frappe.model.with_doc("Branch", frm.doc.std_branch_name, function () {
        let source_doc = frappe.model.get_doc(
          "Branch",
          frm.doc.std_branch_name
        );
        $.each(source_doc.room_details, function (index, source_row) {
          const target_row = frm.add_child("std_room_details");
          target_row.room_number = source_row.room_number;
          target_row.room_bed_capacity = source_row.room_bed_capacity;
          target_row.room_bed_occupied = source_row.room_bed_occupied;
          target_row.bed_availability = source_row.bed_availability;
          frm.refresh_field("std_room_details");
        });
      });
    }
  },
  room_avail_status: function (frm) {
    if (frm.doc.std_branch_name) {
      frm.clear_table("std_room_details");
      frappe.model.with_doc("Branch", frm.doc.std_branch_name, function () {
        let source_doc = frappe.model.get_doc(
          "Branch",
          frm.doc.std_branch_name
        );
        $.each(source_doc.room_details, function (index, source_row) {
          const target_row = frm.add_child("std_room_details");
          target_row.room_number = source_row.room_number;
          target_row.room_bed_capacity = source_row.room_bed_capacity;
          target_row.room_bed_occupied = source_row.room_bed_occupied;
          target_row.bed_availability = source_row.bed_availability;
          frm.refresh_field("std_room_details");
        });
      });
    } else {
      frappe.throw("Pleas select the branch first");
    }
  },
});
