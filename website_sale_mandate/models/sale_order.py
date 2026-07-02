from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("iban", "iban_contact")
    def _compute_show_mandate_action(self):
        mandate_obj = self.env["account.banking.mandate"]
        for order in self:
            mandat_ids = mandate_obj.search(
                [
                    ("partner_id", "=", order.partner_id.id),
                    ("state", "=", "valid"),
                ]
            )
            order.show_mandate_action = False
            if order.iban and order.iban not in mandat_ids.mapped(
                "partner_bank_id.acc_number"
            ):
                order.show_mandate_action = True

    authorize_iban_direct_debit = fields.Boolean("Active Direct Debit (SEPA)")
    show_mandate_action = fields.Boolean(
        "Show Mandate action", compute="_compute_show_mandate_action", store=True
    )
    iban = fields.Char("IBAN")
    iban_contact = fields.Char("Iban Contact")

    @api.multi
    def action_create_partner_mandate(self):
        mandate_obj = self.env["account.banking.mandate"]
        bank_obj = self.env["res.partner.bank"]

        for order in self:
            if order.iban:
                new_bank = bank_obj.create(
                    {
                        "acc_number": order.iban,
                        "type": "iban",
                        "partner_id": order.partner_id.id,
                    }
                )

                mandat_id = mandate_obj.create(
                    {
                        "format": "sepa",
                        "type": "recurrent",
                        "partner_bank_id": new_bank.id,
                        "partner_id": order.partner_id.id,
                        "structure": "CORE",
                        "recurent_sequence_type": "first",
                        "signature_date": datetime.today().strftime("%Y-%m-%d"),
                    }
                )
                if mandat_id:
                    mandat_id.validate()
                order._compute_show_mandate_action()
        return {"type": "ir.actions.act_view_reload"}
