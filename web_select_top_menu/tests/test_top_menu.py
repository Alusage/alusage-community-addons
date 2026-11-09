# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestTopMenu(TransactionCase):
    def setUp(self):
        super().setUp()
        Menu = self.env["ir.ui.menu"]
        self.action = self.env["ir.actions.act_window"].create(
            {
                "name": "Test Partners",
                "res_model": "res.partner",
                "view_mode": "list,form",
            }
        )
        self.env["ir.actions.act_window.view"].create(
            {
                "act_window_id": self.action.id,
                "view_mode": "list",
                "view_id": self.env.ref("base.view_partner_tree").id,
            }
        )
        self.source = Menu.create(
            {
                "name": "Source Menu",
                "sequence": 10,
                "action": "ir.actions.act_window,%s" % self.action.id,
            }
        )
        self.source_child = Menu.create(
            {"name": "Source Child", "parent_id": self.source.id}
        )
        self.container = Menu.create({"name": "Test Container", "is_top_menu": True})
        self.user = self.env["res.users"].create(
            {
                "name": "Top Menu User",
                "login": "top_menu_user",
                "group_ids": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )

    def test_sync_copy_follows_source(self):
        copy = self.source._top_menu_copy_tree(self.container, "sync")
        self.assertTrue(copy.top_menu_sync)
        self.assertEqual(copy.top_menu_source_id, self.source)
        self.assertEqual(copy.action, self.action)
        self.assertEqual(copy.child_id.top_menu_source_id, self.source_child)

        self.source.write({"name": "Renamed Source"})
        self.assertEqual(copy.name, "Renamed Source")

    def test_copy_is_independent(self):
        copy = self.source._top_menu_copy_tree(self.container, "copy")
        self.assertFalse(copy.top_menu_sync)
        self.assertNotEqual(copy.action, self.action)
        self.assertEqual(copy.action.res_model, "res.partner")
        self.assertNotEqual(copy.action.view_ids.view_id, self.action.view_ids.view_id)

        self.source.write({"name": "Renamed Source"})
        self.assertEqual(copy.name, "Source Menu")

    def test_sync_mode_cannot_be_changed(self):
        copy = self.source._top_menu_copy_tree(self.container, "copy")
        with self.assertRaises(UserError):
            copy.write({"top_menu_sync": True})
        self.assertFalse(copy.top_menu_sync)

    def test_copy_includes_hidden_sub_menus(self):
        # Un dossier sans contenu est masqué des listes visibles : il doit
        # tout de même être copié
        self.env["ir.ui.menu"].create(
            {"name": "Empty folder", "parent_id": self.source.id}
        )
        copy = self.source._top_menu_copy_tree(self.container, "copy")
        self.assertIn("Empty folder", copy._top_menu_children().mapped("name"))

    def test_copy_action_with_extension_view(self):
        base_form = self.env.ref("base.view_partner_form")
        extension = self.env["ir.ui.view"].create(
            {
                "name": "Test extension",
                "model": "res.partner",
                "inherit_id": base_form.id,
                "arch": (
                    "<data><xpath expr=\"//field[@name='name']\" "
                    'position="after"/></data>'
                ),
            }
        )
        self.action.view_id = extension
        copy = self.source._top_menu_copy_tree(self.container, "copy")
        self.assertEqual(copy.action.view_id.inherit_id, base_form)

    def test_copy_action_with_url_path(self):
        # Odoo 18 : le chemin d'URL d'une action est unique, la copie ne le reprend pas
        self.action.path = "test-top-menu-path"
        copy = self.source._top_menu_copy_tree(self.container, "copy")
        self.assertFalse(copy.action.path)
        self.assertEqual(self.action.path, "test-top-menu-path")

    def test_user_is_locked_in_container(self):
        self.source._top_menu_copy_tree(self.container, "sync")
        self.user.top_menu_id = self.container
        roots = self.env["ir.ui.menu"].with_user(self.user).get_user_roots()
        self.assertEqual(roots.mapped("name"), ["Source Menu"])
        menus = self.env["ir.ui.menu"].with_user(self.user).load_menus(False)
        self.assertEqual(menus["root"]["children"], roots.ids)
        self.assertNotIn(self.container.id, menus)

    def test_unlink_container_removes_sub_menus(self):
        copy = self.source._top_menu_copy_tree(self.container, "sync")
        child_ids = copy.child_id.ids
        self.container.unlink()
        self.assertFalse(self.env["ir.ui.menu"].browse([copy.id] + child_ids).exists())
        self.assertTrue(self.source.exists())
