import logging

from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.addons.resource.models.resource import HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    can_be_negative = fields.Boolean(
        string="Can be negative",
        help="If checked, the allocation can go negative.",
        default=False,
    )
