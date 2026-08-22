from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    dayflow_employee_code = fields.Char(
        string="Employee ID", readonly=True, copy=False, index=True
    )
    dayflow_joining_date = fields.Date(string="Joining Date")
    dayflow_pan = fields.Char(string="PAN")
    dayflow_uan = fields.Char(string="UAN")
    dayflow_bank_account = fields.Char(string="Bank Account")
    dayflow_bank_name = fields.Char(string="Bank Name")
    dayflow_ifsc = fields.Char(string="IFSC")
    dayflow_location = fields.Char(string="Work Location")
    dayflow_skills = fields.Text(string="Skills")
    dayflow_certifications = fields.Text(string="Certifications")
    dayflow_private_notes = fields.Text(string="Private Information")
    dayflow_initial_password = fields.Char(
        string="Initial Password",
        copy=False,
        groups="dayflow_core.group_dayflow_hr",
    )

    _sql_constraints = [
        (
            "dayflow_employee_code_unique",
            "unique(dayflow_employee_code)",
            "Employee ID must be unique.",
        )
    ]

    @api.model
    def _next_dayflow_serial(self, year):
        count = self.search_count([
            ("dayflow_employee_code", "like", f"OI____{year}%")
        ])
        return count + 1

    @api.model
    def generate_dayflow_employee_code(self, first_name, last_name, joining_date):
        first = "".join(ch for ch in (first_name or "").upper() if ch.isalpha())[:2].ljust(2, "X")
        last = "".join(ch for ch in (last_name or "").upper() if ch.isalpha())[:2].ljust(2, "X")
        year = joining_date.year
        serial = self._next_dayflow_serial(year)
        return f"OI{first}{last}{year}{serial:04d}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("dayflow_employee_code"):
                joining_date = fields.Date.to_date(
                    vals.get("dayflow_joining_date")
                ) or fields.Date.context_today(self)
                name = vals.get("name") or ""
                parts = name.split()
                first = parts[0] if parts else ""
                last = parts[-1] if len(parts) > 1 else ""
                vals["dayflow_employee_code"] = self.generate_dayflow_employee_code(
                    first, last, joining_date
                )
        return super().create(vals_list)

    def write(self, vals):
        if "dayflow_employee_code" in vals:
            raise ValidationError("Employee ID is generated automatically.")
        return super().write(vals)
