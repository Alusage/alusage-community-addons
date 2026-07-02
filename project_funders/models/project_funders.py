from odoo import _, api, fields, models


class ProjectFunders(models.Model):
    _name = "project.funder"
    _description = "Funder and amount for tasks"

    name = fields.Char(compute="_compute_name", string="Name")
    partner_id = fields.Many2one("res.partner", string="Funder", required=True)
    amount = fields.Float("Untaxed Amount", required=True)
    task_id = fields.Many2one("project.task", string="Task")

    @api.depends("partner_id", "amount")
    def _compute_name(self):
        for record in self:
            record.name = "%s (%s)" % (record.partner_id.name, record.amount)
