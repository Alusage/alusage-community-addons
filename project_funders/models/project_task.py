from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    funder_ids = fields.One2many("project.funder", "task_id", string="funder")
    amount_total = fields.Float(compute="_compute_amount_total", string="Amount Total")

    @api.depends("funder_ids")
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.funder_ids.mapped("amount"))
