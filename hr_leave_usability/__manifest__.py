# -*- coding: utf-8 -*-
{
    "name": "HR Leave usability",
    "summary": """
            Permit negative allocation for leave allocation
        """,
    "description": """
    """,
    "author": "Nicolas JEUDY (Alusage)",
    "website": "https://alusage.fr/",
    "category": "Tools",
    "license": "LGPL-3",
    #'currency': 'USD',
    #'price': 0.0,
    "version": "14.0.1.0.1",
    "maintainer": "Nicolas JEUDY",
    "support": "support@alusage.fr",
    "installable": True,
    "application": False,
    "sequence": 1,
    "depends": ["base", "hr", "hr_holidays"],
    "data": [
        "views/hr_leave_type_view.xml",
    ],
    "qweb": [],
}
