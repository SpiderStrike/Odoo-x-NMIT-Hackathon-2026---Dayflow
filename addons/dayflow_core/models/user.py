from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        readonly=True,
        copy=False,
    )
