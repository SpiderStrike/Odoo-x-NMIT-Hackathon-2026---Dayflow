from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    dayflow_status = fields.Selection(
        [
            ("present", "Present"),
            ("late", "Late"),
            ("half_day", "Half Day"),
        ],
        compute="_compute_dayflow_status",
        store=True,
    )
    dayflow_extra_hours = fields.Float(
        string="Extra Hours",
        compute="_compute_dayflow_extra_hours",
        store=True,
    )

    @api.depends("worked_hours")
    def _compute_dayflow_status(self):
        for record in self:
            if not record.check_in:
                record.dayflow_status = False
            elif record.worked_hours < 4:
                record.dayflow_status = "half_day"
            else:
                record.dayflow_status = "present"

    @api.depends("worked_hours")
    def _compute_dayflow_extra_hours(self):
        for record in self:
            record.dayflow_extra_hours = max(record.worked_hours - 8.0, 0.0)
