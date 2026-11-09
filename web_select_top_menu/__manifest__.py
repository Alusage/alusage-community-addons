# pylint: disable=missing-docstring
# Copyright 2021 Nicolas JEUDY
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Web Select Top Menu",
    "summary": """
        Select top menus per user to create simple backend entry
        By default top menus are menu that have no parent_id""",
    "version": "20.0.2.0.0",
    "license": "AGPL-3",
    "author": "Nicolas JEUDY, ArPol",
    "website": "https://github.com/Alusage/odoo-web-addons",
    "depends": [
        "web",
        "base",
    ],
    "data": [
        "security/ir.access.csv",
        "views/res_users.xml",
        "views/ir_ui_menu_views.xml",
        "views/top_menu_add_wizard_views.xml",
    ],
    "demo": [],
    "installable": True,
}
