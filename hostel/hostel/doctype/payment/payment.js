// Copyright (c) 2022, milan thapa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment", {
  pmt_branch: function (frm) {
    if (frm.doc.pmt_branch) {
      frappe.db.get_doc("Branch", frm.doc.pmt_branch).then((doc) => {
        let rooms_list = doc.room_details;
        let valid_rooms_list = rooms_list.map(function (room) {
          return room.room_number;
        });
        // console.log(valid_rooms_list)
        frm.set_df_property("pmt_room", "options", valid_rooms_list);
        frm.refresh_field("pmt_room");
        frm.set_query("pmt_std", function () {
          return {
            filters: [
              ["std_branch_name", "=", frm.doc.pmt_branch],
              ["std_room_number", "=", frm.doc.pmt_room],
            ],
          };
        });
      });
    }
  },
  pmt_std: function (frm) {
    if (frm.doc.pmt_std) {
      frappe.db
        .get_value("Fee Management", { std_name: frm.doc.pmt_std }, [
          "std_rem_bal",
          "std_fine_amt",
          "std_extras",
        ])
        .then((r) => {
          let values = r.message;
          frm.set_value("pmt_rem_balance", values.std_rem_bal);
          frm.refresh_field("pmt_rem_balance");
        });
    }
  },
  pmt_fee_cat: function (frm) {
    if (frm.doc.pmt_std) {
      frappe.db
        .get_value("Fee Management", { std_name: frm.doc.pmt_std }, [
          "std_rem_bal",
          "std_fine_amt",
          "std_extras",
        ])
        .then((r) => {
          let values = r.message;
          let fee_cat_list = [
            "Monthly Fee",
            "Admission Fee",
            "Security Deposit",
          ];
          if (fee_cat_list.indexOf(frm.doc.pmt_fee_cat) !== -1) {
            frm.set_value("pmt_rem_balance", values.std_rem_bal);
            frm.refresh_field("pmt_rem_balance");
          } else if (frm.doc.pmt_fee_cat == "Fine") {
            frm.set_value("pmt_rem_fine", values.std_fine_amt);
            frm.refresh_field("pmt_rem_fine");
          } else {
            frm.set_value("pmt_extra_amt", values.std_extras);
            frm.refresh_field("pmt_extra_amt");
          }
        });
    }
  },
});
