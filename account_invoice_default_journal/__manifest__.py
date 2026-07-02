{
    "name": "account_invoice_default_journal",
    "summary": """
        Select default journal on invoice with the new field `force_journal` on `product.product` model
        """,
    "description": """
   ::image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
account_invoice_default_journal
===============================

Module add some default setup for french lcc company

Installation
============

Just install account_invoice_default_journal, all dependencies will be installed by default.

Configuration
=============

No configuration needed on this addon.

Usage
=====

Go to the product form view and set the `force_journal_id` field.
An invoice can not have two product with force_journal_id that are different. You should create 2 invoices in this case.

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Stéphan SAINLEGER <https://github.com/stephansainleger>
* Nicolas JEUDY <https://github.com/njeudy>

Funders
-------

The development of this module has been financially supported by:

* Lokavaluto (https://lokavaluto.fr)
* Mycéliandre (https://myceliandre.fr)
* Elabore (https://elabore.coop)

Maintainer
----------

* Nicolas JEUDY <https://github.com/njeudy>

""",
    "author": "Nicolas JEUDY",
    "website": "https://myceliandre.fr",
    "category": "Accounting",
    "version": "12.0.1.0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "account"],
    # always loaded
    "data": [
        "views/product_template_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
