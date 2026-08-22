from odoo import fields, models


class DayflowNotification(models.Model):
    _name = "dayflow.notification"
    _description = "Dayflow Notification"

    name = fields.Char(required=True)
    recipient_id = fields.Many2one("res.users", required=True)
    message = fields.Text(required=True)
    notification_type = fields.Selection(
        [("info", "Information"), ("success", "Success"), ("warning", "Warning")],
        default="info",
        required=True,
    )
    is_read = fields.Boolean(default=False)
