from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    dayflow_employee_code = fields.Char(
        string="Employee ID",
        readonly=True,
        copy=False,
        index=True,
    )

    dayflow_joining_date = fields.Date(
        string="Date of Joining",
        tracking=True,
    )

    dayflow_employment_status = fields.Selection(
        [
            ("active", "Active"),
            ("on_leave", "On Leave"),
            ("inactive", "Inactive"),
            ("terminated", "Terminated"),
        ],
        string="Employment Status",
        default="active",
        required=True,
        tracking=True,
    )

    dayflow_pan = fields.Char(
        string="PAN",
        groups="dayflow_core.group_dayflow_hr",
    )

    dayflow_uan = fields.Char(
        string="UAN",
        groups="dayflow_core.group_dayflow_hr",
    )

    dayflow_bank_account = fields.Char(
        string="Bank Account",
        groups="dayflow_core.group_dayflow_hr",
    )

    dayflow_bank_name = fields.Char(
        string="Bank Name",
        groups="dayflow_core.group_dayflow_hr",
    )

    dayflow_ifsc = fields.Char(
        string="IFSC",
        groups="dayflow_core.group_dayflow_hr",
    )

    dayflow_location = fields.Char(
        string="Work Location",
    )

    dayflow_skills = fields.Text(
        string="Skills",
    )

    dayflow_certifications = fields.Text(
        string="Certifications",
    )

    dayflow_private_notes = fields.Text(
        string="Private HR Notes",
        groups="dayflow_core.group_dayflow_hr",
    )

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
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]

        for vals in vals_list:
            if not vals.get("dayflow_employee_code"):
                vals["dayflow_employee_code"] = sequence.next_by_code(
                    "dayflow.employee"
                )

        return super().create(vals_list)

    def write(self, vals):
        if "dayflow_employee_code" in vals:
            for employee in self:
                if (
                    employee.dayflow_employee_code
                    and vals["dayflow_employee_code"]
                    != employee.dayflow_employee_code
                ):
                    raise UserError(
                        _("Employee ID cannot be changed.")
                    )

        return super().write(vals)

    @api.constrains("dayflow_joining_date", "birthday")
    def _check_employee_dates(self):
        today = fields.Date.context_today(self)

        for employee in self:
            if (
                employee.dayflow_joining_date
                and employee.dayflow_joining_date > today
            ):
                raise ValidationError(
                    _("Date of Joining cannot be in the future.")
                )

            if employee.birthday and employee.birthday > today:
                raise ValidationError(
                    _("Date of Birth cannot be in the future.")
                )

            if (
                employee.birthday
                and employee.dayflow_joining_date
                and employee.birthday > employee.dayflow_joining_date
            ):
                raise ValidationError(
                    _("Date of Birth cannot be after Date of Joining.")
                )

    def action_create_user_account(self):
        self.ensure_one()

        if not self.dayflow_employee_code:
            raise UserError(
                _("The employee must have an Employee ID.")
            )

        if self.user_id:
            raise UserError(
                _("This employee already has an Odoo user account.")
            )

        password = self.dayflow_initial_password

        if not password:
            raise UserError(
                _(
                    "Enter an initial password before creating "
                    "the user account."
                )
            )

        login = self.dayflow_employee_code

        if self.env["res.users"].sudo().search_count(
            [("login", "=", login)]
        ):
            raise UserError(
                _("An Odoo user with login '%s' already exists.")
                % login
            )

        user = self.env["res.users"].sudo().create(
            {
                "name": self.name,
                "login": login,
                "password": password,
                "email": self.work_email,
                "employee_id": self.id,
            }
        )

        employee_group = self.env.ref(
            "dayflow_core.group_dayflow_employee"
        )

        user.sudo().write(
            {
                "groups_id": [(4, employee_group.id)],
            }
        )

        self.sudo().write(
            {
                "user_id": user.id,
                "dayflow_initial_password": False,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "res.users",
            "res_id": user.id,
            "view_mode": "form",
            "target": "current",
        }
