from odoo import api, models


class DayflowDashboard(models.AbstractModel):
    _name = "dayflow.dashboard"
    _description = "Dayflow Dashboard"

    @api.model
    def get_employee_metrics(self):
        employee = self.env.user.employee_id
        Attendance = self.env["hr.attendance"]
        Leave = self.env["hr.leave"]
        if not employee:
            return {"attendance": 0, "leave": 0}
        return {
            "attendance": Attendance.search_count([("employee_id", "=", employee.id)]),
            "leave": Leave.search_count([("employee_id", "=", employee.id)]),
        }
