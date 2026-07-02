from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    forced_journal_id = fields.Many2one(
        "account.journal",
        company_dependent=True,
        check_company=True,
        string="Forced sale journal",
        domain="[('type', '=', 'sale')]",
    )
    forced_purchase_journal_id = fields.Many2one(
        "account.journal",
        company_dependent=True,
        check_company=True,
        string="Forced purchase journal",
        domain="[('type', '=', 'purchase')]",
    )
