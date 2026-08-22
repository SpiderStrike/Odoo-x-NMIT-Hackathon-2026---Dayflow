from calendar import monthrange
from datetime import date

from odoo import api, fields, models


class DayflowPayroll(models.Model):
    _name = "dayflow.payroll"
    _description = "Dayflow Payroll"
    _order = "period_start desc, employee_id"

    employee_id = fields.Many2one("hr.employee", required=True, ondelete="cascade")
    salary_structure_id = fields.Many2one(
        "dayflow.salary.structure", required=True, ondelete="restrict"
    )
    period_start = fields.Date(required=True)
    period_end = fields.Date(required=True)
    calendar_days = fields.Integer(compute="_compute_days", store=True)
    unpaid_leave_days = fields.Float(compute="_compute_days", store=True)
    payable_days = fields.Float(compute="_compute_days", store=True)
    gross_salary = fields.Monetary(related="salary_structure_id.gross_salary", store=True)
    pf = fields.Monetary(related="salary_structure_id.pf", store=True)
    professional_tax = fields.Monetary(
        related="salary_structure_id.professional_tax", store=True
    )
    net_salary = fields.Monetary(compute="_compute_net", store=True)
    currency_id = fields.Many2one(
        "res.currency",
        related="salary_structure_id.currency_id",
        store=True,
    )
    state = fields.Selection(
        [("draft", "Draft"), ("processed", "Processed")],
        default="draft",
    )

    @api.depends("period_start", "period_end", "employee_id")
    def _compute_days(self):
        Leave = self.env["hr.leave"]
        Attendance = self.env["hr.attendance"]
        for rec in self:
            if not rec.period_start or not rec.period_end:
                rec.calendar_days = 0
                rec.unpaid_leave_days = 0
                rec.payable_days = 0
                continue
            days = (rec.period_end - rec.period_start).days + 1
            unpaid = 0.0
            leaves = Leave.search([
                ("employee_id", "=", rec.employee_id.id),
                ("state", "=", "validate"),
                ("request_date_from", "<=", rec.period_end),
                ("request_date_to", ">=", rec.period_start),
                ("dayflow_leave_type", "=", "unpaid"),
            ])
            unpaid = sum(leaves.mapped("number_of_days"))
            attendance_count = Attendance.search_count([
                ("employee_id", "=", rec.employee_id.id),
                ("check_in", ">=", f"{rec.period_start} 00:00:00"),
                ("check_in", "<=", f"{rec.period_end} 23:59:59"),
            ])
            rec.calendar_days = days
            rec.unpaid_leave_days = unpaid
            rec.payable_days = max(days - unpaid, 0.0)

    @api.depends("gross_salary", "pf", "professional_tax", "payable_days", "calendar_days")
    def _compute_net(self):
        for rec in self:
            ratio = rec.payable_days / rec.calendar_days if rec.calendar_days else 0
            rec.net_salary = max(
                (rec.gross_salary * ratio) - rec.pf - rec.professional_tax, 0.0
            )
