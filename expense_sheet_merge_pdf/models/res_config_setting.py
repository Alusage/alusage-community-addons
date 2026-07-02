from odoo import fields, models, api


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    expense_merge_pdf_report_ids = fields.Many2many(
        related="company_id.expense_merge_pdf_report_ids",
        readonly=False,
        domain="[('model', '=', 'hr.expense.sheet'),('report_type','=','qweb-pdf')]",
        string="Expense reports",
    )
