from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DayflowSalaryStructure(models.Model):
    _name = "dayflow.salary.structure"
    _description = "Dayflow Salary Structure"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("hr.employee", required=True, ondelete="cascade")
    wage = fields.Monetary(required=True)
    basic_salary = fields.Monetary(compute="_compute_components", store=True)
    hra = fields.Monetary(compute="_compute_components", store=True)
    standard_allowance = fields.Monetary(compute="_compute_components", store=True)
    performance_bonus = fields.Monetary(compute="_compute_components", store=True)
    lta = fields.Monetary(compute="_compute_components", store=True)
    fixed_allowance = fields.Monetary(compute="_compute_components", store=True)
    gross_salary = fields.Monetary(compute="_compute_components", store=True)
    pf = fields.Monetary(compute="_compute_components", store=True)
    professional_tax = fields.Monetary(compute="_compute_components", store=True)
    net_salary = fields.Monetary(compute="_compute_components", store=True)
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    @api.depends("wage")
    def _compute_components(self):
        for rec in self:
            wage = rec.wage or 0.0
            basic = wage * 0.50
            hra = basic * 0.50
            # The flow requires components to recalculate from wage and not exceed wage.
            # Remaining components are represented as a configurable-safe baseline.
            standard = max(wage - basic - hra, 0.0)
            performance = 0.0
            lta = 0.0
            fixed = 0.0
            gross = min(basic + hra + standard + performance + lta + fixed, wage)
            pf = basic * 0.12
            professional_tax = min(200.0, gross)
            net = max(gross - pf - professional_tax, 0.0)

            rec.basic_salary = basic
            rec.hra = hra
            rec.standard_allowance = standard
            rec.performance_bonus = performance
            rec.lta = lta
            rec.fixed_allowance = fixed
            rec.gross_salary = gross
            rec.pf = pf
            rec.professional_tax = professional_tax
            rec.net_salary = net

    @api.constrains("wage")
    def _check_wage(self):
        for rec in self:
            if rec.wage < 0:
                raise ValidationError("Wage cannot be negative.")
