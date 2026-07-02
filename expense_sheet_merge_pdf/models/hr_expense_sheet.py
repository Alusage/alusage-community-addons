import base64

from odoo import _, fields, models


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    expense_merge_pdf_attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        string="Attachment Merge",
        relation="expense_merge_attachment_id",
    )

    def action_export_merged_pdf(self):
        self.ensure_one()
        pdf = self.env.ref(
            "hr_expense.action_report_hr_expense_sheet"
        )._render_qweb_pdf([self.id])[0]
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        attachment_obj = self.env["ir.attachment"]
        attachment_id = attachment_obj.create({"name": "name_test_NJ", "datas": pdf})
        download_url = "/web/content/" + str(attachment_id.id) + "?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }
