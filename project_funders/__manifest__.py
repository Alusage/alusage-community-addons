# Copyright 2022 Nicolas Jeudy (Alusage)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "project_funders",
    "version": "14.0.0.1.0",
    "author": "Alusage",
    "website": "https://alusage.fr",
    "data": [
        # "security/security.xml",
        # "security/ir.model.access.csv",
        # "views/menu.xml",
        # "data/data.xml",
    ],
    "author": "Alusage, Elabore",
    "maintainer": "Nicolas Jeudy",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": " Odoo module.",
    "description": """
   :image: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
===============
project_funders
===============

Add list of funder and corresponding amount to project task.

Installation
============

Use Odoo normal module installation procedure to install
``project_funders``.

Known issues / Roadmap
======================

None yet.

Bug Tracker
===========

Bugs are tracked on `our issues website <https://github.com/elabore-coop/project-tools/issues>`_. In case of
trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Nicolas Jeudy <https://github.com/njeudy>
* Valentin Lab

Funders
-------
The development of this module has been financially supported by:
* Alusage (https://alusage.fr)


Maintainer
----------
This module is maintained by Alusage and Elabore.

""",
    # any module necessary for this one to work correctly
    "depends": ["base", "project"],
    "qweb": [
        # "static/src/xml/*.xml",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": ["security/ir.model.access.csv", "views/project_task_view.xml"],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}
