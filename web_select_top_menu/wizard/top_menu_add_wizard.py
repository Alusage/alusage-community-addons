# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class TopMenuAddWizard(models.TransientModel):
    _name = "top.menu.add.wizard"
    _description = "Add an Existing Menu to a Top Menu"

    parent_id = fields.Many2one(
        "ir.ui.menu",
        string="Parent Menu",
        required=True,
        ondelete="cascade",
        context={"ir.ui.menu.full_list": True},
    )
    source_id = fields.Many2one(
        "ir.ui.menu",
        string="Source Menu",
        required=True,
        domain=[("is_top_menu", "=", False)],
        context={"ir.ui.menu.full_list": True},
    )
    mode = fields.Selection(
        [
            ("sync", "Synchronized with the source menu"),
            ("copy", "Duplicated (independent copy)"),
        ],
        string="Mode",
        required=True,
        default="sync",
    )
    include_children = fields.Boolean(string="Include Sub-menus", default=True)

    def action_add_menu(self):
        self.ensure_one()
        if not self.parent_id._get_top_menu_root().is_top_menu:
            raise UserError(_("The parent menu must belong to a top menu container."))
        if self.parent_id.parent_path.startswith(self.source_id.parent_path):
            raise UserError(
                _("A menu cannot be added inside itself or one of its sub-menus.")
            )
        self.source_id._top_menu_copy_tree(
            self.parent_id, self.mode, self.include_children
        )
        return {"type": "ir.actions.client", "tag": "reload"}
