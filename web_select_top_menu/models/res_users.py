# pylint: disable=missing-docstring
# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    top_menu_id = fields.Many2one("ir.ui.menu", string="Top Menu")
