import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DayflowEmployee(models.Model):
    _name = "dayflow.employee"
    _description = "Dayflow Employee"

    name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    date_of_joining = fields.Date(
        string="Date of Joining",
        required=True,
        default=fields.Date.context_today,
    )
    employee_id = fields.Char(
        string="Employee ID",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("employee_id", _("New")) == _("New"):
                # Clean up names to uppercase alphabetic characters
                first_name = re.sub(r"[^A-Z]", "", (vals.get("name") or "").upper())
                last_name = re.sub(r"[^A-Z]", "", (vals.get("last_name") or "").upper())

                if not first_name or not last_name:
                    raise ValidationError(
                        _("First Name and Last Name must contain valid alphabetic characters.")
                    )

                # Extract first 2 characters (pad with 'X' if length < 2)
                fn_part = (first_name[:2]).ljust(2, "X")
                ln_part = (last_name[:2]).ljust(2, "X")

                # Extract joining year
                joining_date = fields.Date.from_string(vals.get("date_of_joining"))
                if not joining_date:
                    raise ValidationError(_("Date of Joining is required for Employee ID generation."))
                
                year_str = str(joining_date.year)

                # Obtain next 4-digit serial from sequence for the specific joining date
                serial_num = self.env["ir.sequence"].next_by_code(
                    "dayflow.employee.code",
                    sequence_date=joining_date
                ) or "0001"

                # Standard sequence returns padded number string (e.g. '0001')
                # Take last 4 digits in case sequence returns prefixed text
                serial_part = serial_num[-4:]

                # Construct exact Employee ID format: OIJODO20220001
                vals["employee_id"] = f"OI{fn_part}{ln_part}{year_str}{serial_part}"

        return super(DayflowEmployee, self).create(vals_list)
