# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def get_forced_journal(self):
        for record in self:
            if record.type in ["out_invoice", "out_refund"]:
                forced_journal_ids = record.invoice_line_ids.mapped(
                    "product_id.forced_journal_id"
                )
            if record.type in ["in_invoice", "in_refund"]:
                forced_journal_ids = record.invoice_line_ids.mapped(
                    "product_id.forced_purchase_journal_id"
                )
            if forced_journal_ids and len(forced_journal_ids) > 1:
                raise UserError(
                    _("You can not have 2 forced journals on the same invoice !")
                )
            if forced_journal_ids and len(forced_journal_ids) == 1:
                return forced_journal_ids[0]
            else:
                return record.journal_id

    @api.model
    def create(self, vals):
        invoice_id = super(AccountInvoice, self).create(vals)
        forced_journal_id = self.env["account.journal"]
        if invoice_id and invoice_id.invoice_line_ids:
            forced_journal_id = invoice_id.get_forced_journal()
            if forced_journal_id:
                invoice_id.write(
                    {
                        "journal_id": forced_journal_id.id,
                    }
                )
        return invoice_id

    @api.model
    def write(self, vals):
        if not vals.get("journal_id", False):
            for record in self:
                if record.invoice_line_ids:
                    forced_journal_id = record.get_forced_journal()
                    if forced_journal_id:
                        vals["journal_id"] = forced_journal_id.id

        super(AccountInvoice, self).write(vals)
