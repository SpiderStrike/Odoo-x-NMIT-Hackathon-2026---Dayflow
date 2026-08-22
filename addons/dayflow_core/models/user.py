from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create_dayflow_user(self, employee):
        if not employee.user_id:
            user = self.create({
                "name": employee.name,
                "login": employee.dayflow_employee_code,
                "email": employee.work_email,
                "employee_id": employee.id,
                "groups_id": [(6, 0, [
                    self.env.ref("dayflow_core.group_dayflow_employee").id
                ])],
            })
            employee.user_id = user.id
            return user
        return employee.user_id
