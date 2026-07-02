{
    'name': "product_template_openfood",

    'summary': """
        Connect to openfood project to import product data.
        """,

    'description': """
   ::image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
product_template_openfood
=========================


Installation
============

Just install lcc_partner_gogocartojs, all dependencies will be installed by default.

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/Lokavaluto/lokavaluto-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Nicolas JEUDY

Funders
-------

The development of this module has been financially supported by:

* Mycéliandre (https://myceliandre.fr)

Maintainer
----------

This module is maintained by MYCELIANDRE.

MYCELIANDRE, is SAS SCIC (Coopérative)

""",

    'author': "Myceliandre",
    'website': "https://myceliandre.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
