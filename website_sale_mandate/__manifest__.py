{
    "name": "Ask SEPA mandate on checkout",
    "version": "12.0.1.1.0",
    "description": "Ask SEPA mandate on website sale checkout",
    "summary": "Ask SEPA mandate on website sale checkout",
    "author": "Nicolas JEUDY",
    "website": "https://github.com/Alusage/odoo-usability-addons",
    "license": "LGPL-3",
    "category": "Generic Modules",
    "depends": [
        "base",
        "website_sale",
        "website_form",
        "account_banking_mandate",
        "account_banking_sepa_direct_debit",
        "web_ir_actions_act_view_reload",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": False,
}
