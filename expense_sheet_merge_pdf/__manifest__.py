{
    "name": "Merge attachment PDF on expense Sheet",
    "version": "13.0.1.0.1",
    "description": "Export expense sheet report merged with attachments",
    "summary": "Export expense sheet report merged with attachments",
    "author": "Nicolas JEUDY",
    "website": "https://nj.0k.io",
    "license": "LGPL-3",
    "category": "Human Resources",
    "depends": ["base", "hr_expense"],
    "data": [
        "views/hr_expense_view.xml",
        "views/res_config_setting.xml",
    ],
    "installable": True,
    "application": False,
}
