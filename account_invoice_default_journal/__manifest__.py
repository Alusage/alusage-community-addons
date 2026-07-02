{
    "name": "account_invoice_default_journal",
    "summary": """
        Select default journal on invoice with the new field `force_journal` on `product.product` model
        """,
    "author": "Nicolas JEUDY",
    "website": "https://myceliandre.fr",
    "category": "Accounting",
    "version": "16.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "account"],
    # always loaded
    "data": [
        "views/product_template_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
