from odoo import _, api, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
class AccountInvoice(models.Model):
    _inherit = "account.move"

    def get_forced_journal(self):
        for record in self:
            forced_journal_ids = []
            if record.move_type in {"out_invoice", "out_refund"}:
                forced_journal_ids = record.invoice_line_ids.mapped(
                    "product_id.forced_journal_id",
                )
            if record.move_type in {"in_invoice", "in_refund"}:
                forced_journal_ids = record.invoice_line_ids.mapped(
                    "product_id.forced_purchase_journal_id",
                )
            if forced_journal_ids and len(forced_journal_ids) > 1:
                raise UserError(
                    _("You can not have 2 forced journals on the same invoice !"),
                )
            if forced_journal_ids and len(forced_journal_ids) == 1:
                return forced_journal_ids[0]
            return record.journal_id
        return None

    def _search_default_journal(self):
        res = super()._search_default_journal()
        forced_journal_id = self.get_forced_journal()
        if forced_journal_id:
            return forced_journal_id
        else:
            return res