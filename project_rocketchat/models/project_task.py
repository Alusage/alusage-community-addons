from odoo import _, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "rocketchat.thread.mixin"]
