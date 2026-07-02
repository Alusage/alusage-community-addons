# pylint: disable=missing-docstring
# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    @api.returns('self')
    def get_user_roots(self):
        """ Return all root menu ids visible for the user.
        :return: the root menu ids
        :rtype: list(int)
        """
        if self.env.user.top_menu_id:
            return self.search([('parent_id', '=', self.env.user.top_menu_id.id)])
        else:
            return self.search([('parent_id', '=', False)])
