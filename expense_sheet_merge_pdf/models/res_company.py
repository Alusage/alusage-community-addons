from odoo import fields, models, api


class resCompany(models.Model):
    _inherit = "res.company"

    expense_merge_pdf_report_ids = fields.Many2many(
        comodel_name="ir.actions.report",
        relation="epense_merge_pdf_company_report_rel",
        string="Expenses Sheet report",
    )
