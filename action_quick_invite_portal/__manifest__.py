# Copyright 2023 Alusage SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Action Quick Invite Portal",
    "summary": "Force all partner in portal invite list without manually check in_portal boolean",
    "version": "14.0.0.1.0",
    "development_status": "Alpha",
    "category": "Tools",
    "website": "https://github.com/Alusage/odoo-usability-addons",
    "author": "Nicolas JEUDY, Alusage SAS",
    "maintainers": ["njeudy"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "preloadable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "portal"
    ],
    "excludes": [
    ],
    "data": [
        "wizards/wizard_model_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ],
}
