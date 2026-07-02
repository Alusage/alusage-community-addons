import logging

from odoo import api, fields, models, _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class AccountAccount(models.Model):
    _inherit = "account.account"

    exclude_from_bank_reconcile = fields.Boolean("Exclude from bank reconcile")