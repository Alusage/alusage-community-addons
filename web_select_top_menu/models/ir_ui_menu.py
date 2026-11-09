# pylint: disable=missing-docstring
# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Champs repris par les copies synchronisées lorsque l'original change
SYNC_FIELDS = ("name", "sequence", "action", "group_ids")
FULL_LIST_CONTEXT = {"ir.ui.menu.full_list": True, "active_test": False}


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    is_top_menu = fields.Boolean(
        string="Top Menu Container",
        help="Root of a simplified environment. Its sub-menus are the applications "
        "shown to the users who have this menu as their top menu.",
    )
    top_menu_user_ids = fields.One2many(
        "res.users", "top_menu_id", string="Users", readonly=True
    )
    top_menu_source_id = fields.Many2one(
        "ir.ui.menu",
        string="Source Menu",
        ondelete="set null",
        copy=False,
        index=True,
    )
    top_menu_sync = fields.Boolean(
        string="Synchronized",
        copy=False,
        help="Synchronized copies follow the name, sequence, action and access "
        "groups of their source menu.",
    )

    @api.model
    def get_user_roots(self):
        """Return all root menu ids visible for the user.
        :return: the root menu ids
        :rtype: list(int)
        """
        if self.env.user.top_menu_id:
            return self.search([("parent_id", "=", self.env.user.top_menu_id.id)])
        return self.search([("parent_id", "=", False)])

    def write(self, values):
        if "top_menu_sync" in values and not self.env.context.get("top_menu_no_sync"):
            raise UserError(
                _(
                    "The synchronized mode is set when the menu is added and "
                    "cannot be changed."
                )
            )
        res = super().write(values)
        sync_values = {
            key: value for key, value in values.items() if key in SYNC_FIELDS
        }
        if sync_values and not self.env.context.get("top_menu_no_sync"):
            copies = self.with_context(FULL_LIST_CONTEXT).search(
                [("top_menu_source_id", "in", self.ids), ("top_menu_sync", "=", True)]
            )
            if copies:
                copies.with_context(top_menu_no_sync=True).write(sync_values)
        return res

    def unlink(self):
        # Supprimer un menu d'arborescence supprime aussi ses sous-menus : sinon
        # Odoo les remonterait à la racine et ils apparaîtraient pour tous.
        menus = self._top_menu_with_descendants()
        # Les copies qui pointent vers les menus supprimés deviennent indépendantes
        copies = self.with_context(FULL_LIST_CONTEXT).search(
            [("top_menu_source_id", "in", menus.ids), ("id", "not in", menus.ids)]
        )
        if copies:
            copies.with_context(top_menu_no_sync=True).write(
                {"top_menu_source_id": False, "top_menu_sync": False}
            )
        return super(IrUiMenu, menus).unlink()

    def _top_menu_with_descendants(self):
        containers = self.with_context(FULL_LIST_CONTEXT).search(
            [("is_top_menu", "=", True)]
        )
        container_ids = set(containers.ids)
        inside_ids = [
            menu.id
            for menu in self
            if container_ids
            & {int(item) for item in (menu.parent_path or "").split("/") if item}
        ]
        if not inside_ids:
            return self
        return self | self.with_context(FULL_LIST_CONTEXT).search(
            [("id", "child_of", inside_ids)]
        )

    def _get_top_menu_root(self):
        self.ensure_one()
        menu = self
        while menu.parent_id:
            menu = menu.parent_id
        return menu

    def _top_menu_action_ref(self):
        self.ensure_one()
        if not self.action:
            return False
        return "%s,%s" % (self.action._name, self.action.id)

    def _top_menu_sync_values(self, origin):
        return {
            "name": origin.name,
            "sequence": origin.sequence,
            "action": origin._top_menu_action_ref(),
            "group_ids": [(6, 0, origin.group_ids.ids)],
        }

    @api.model
    def _top_menu_copy_view(self, view, inherit_id=None):
        """Copier une vue et ses extensions : la copie ne dépend plus de l'original.

        Une vue d'extension garde son parent d'origine (Odoo refuse une extension
        sans parent).
        """
        if inherit_id is None:
            inherit_id = view.inherit_id.id
        new_view = view.copy({"inherit_id": inherit_id})
        extensions = (
            self.env["ir.ui.view"]
            .with_context(active_test=False)
            .search([("inherit_id", "=", view.id)])
        )
        for extension in extensions:
            self._top_menu_copy_view(extension, new_view.id)
        return new_view

    def _top_menu_duplicate_action(self):
        self.ensure_one()
        action = self.action
        if not action:
            return False
        default = {
            "name": "%s (copy)" % action.name,
            "binding_model_id": False,
            "path": False,
        }
        is_window = action._name == "ir.actions.act_window"
        if is_window:
            default.update(
                {"view_ids": [(5, 0, 0)], "view_id": False, "search_view_id": False}
            )
        duplicate = action.copy(default)
        if is_window:
            duplicate.write(
                {
                    "view_id": action.view_id
                    and self._top_menu_copy_view(action.view_id).id,
                    "search_view_id": action.search_view_id
                    and self._top_menu_copy_view(action.search_view_id).id,
                    "view_ids": [
                        (
                            0,
                            0,
                            {
                                "sequence": line.sequence,
                                "view_mode": line.view_mode,
                                "multi": line.multi,
                                "view_id": line.view_id
                                and self._top_menu_copy_view(line.view_id).id,
                            },
                        )
                        for line in action.view_ids
                    ],
                }
            )
        return "%s,%s" % (duplicate._name, duplicate.id)

    def _top_menu_copy_tree(self, parent, mode, include_children=True):
        """Copier ce menu (et ses sous-menus) sous `parent`.

        mode 'sync' : la copie référence l'origine (même action, mêmes vues,
        mêmes groupes).
        mode 'copy' : la copie est indépendante (action et vues dupliquées).
        """
        self.ensure_one()
        if mode == "sync":
            origin = (
                self.top_menu_source_id
                if self.top_menu_sync and self.top_menu_source_id
                else self
            )
            values = self._top_menu_sync_values(origin)
            values.update({"top_menu_source_id": origin.id, "top_menu_sync": True})
        else:
            origin = self
            values = {
                "name": self.name,
                "sequence": self.sequence,
                "action": self._top_menu_duplicate_action(),
                "group_ids": [(6, 0, self.group_ids.ids)],
                "top_menu_source_id": self.id,
                "top_menu_sync": False,
            }
        new_menu = self.create(dict(values, parent_id=parent.id, is_top_menu=False))
        if include_children:
            for child in origin._top_menu_children():
                child._top_menu_copy_tree(new_menu, mode)
        return new_menu

    def _top_menu_children(self):
        """Tous les sous-menus, y compris ceux masqués pour l'utilisateur courant."""
        return self.with_context(FULL_LIST_CONTEXT).child_id

    def _top_menu_sync_from_origin(self):
        """Mettre à jour une copie synchronisée depuis son origine, sous-menus
        compris."""
        self.ensure_one()
        origin = self.top_menu_source_id
        self.write(self._top_menu_sync_values(origin))
        for origin_child in origin._top_menu_children():
            synced = self._top_menu_children().filtered(
                lambda menu, origin_child=origin_child: menu.top_menu_sync
                and menu.top_menu_source_id == origin_child
            )
            if synced:
                synced[0]._top_menu_sync_from_origin()
            else:
                origin_child._top_menu_copy_tree(self, "sync")

    def _top_menu_sync_all(self):
        for child in self._top_menu_children():
            if child.top_menu_sync and child.top_menu_source_id:
                child._top_menu_sync_from_origin()
            else:
                child._top_menu_sync_all()

    def action_sync_from_source(self):
        self._top_menu_sync_all()
        return True

    def action_open_menu(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Top Menu Item"),
            "res_model": "ir.ui.menu",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref("web_select_top_menu.top_menu_form_view").id,
            "target": "current",
        }

    def action_open_top_menu_add_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Add an Existing Menu"),
            "res_model": "top.menu.add.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_parent_id": self.id},
        }
