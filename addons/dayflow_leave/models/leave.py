from odoo import fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    dayflow_leave_type = fields.Selection(
        [
            ("paid", "Paid Time Off"),
            ("sick", "Sick Leave"),
            ("unpaid", "Unpaid Leave"),
        ],
        string="Dayflow Leave Type",
        required=True,
        default="paid",
    )
    dayflow_medical_certificate = fields.Binary(
        string="Medical Certificate",
        attachment=True,
    )
    dayflow_medical_certificate_name = fields.Char(
        string="Medical Certificate Filename"
    )
    dayflow_hr_comment = fields.Text(string="HR Comment")
