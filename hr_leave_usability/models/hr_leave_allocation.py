import logging

from odoo import api,fields, models

_logger = logging.getLogger(__name__)


class HolidaysAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    can_be_negative = fields.Boolean(
        string="Can be negative",
        help="If checked, the allocation can go negative.",
        default=False,
    )

    @api.onchange('holiday_status_id')
    def _onchange_holiday_status_id (self):
        if self.holiday_status_id :
            self.can_be_negative = self.holiday_status_id.can_be_negative
    _sql_constraints = [
         (
            "duration_check",
            "CHECK (( number_of_days >= 0 ) or (can_be_negative = True))",
            "The number of days must be greater than 0.",
            
        ),
    ]
