{
    'name': 'My PWA App - Portail Gamifié',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Progressive Web App pour utilisateurs portail avec gamification MTG',
    'description': """
        Application Progressive Web App pour utilisateurs portail Odoo avec système de gamification
        médiéval-fantastique inspiré de Magic: The Gathering.

        Fonctionnalités principales:
        - Interface thématique Magic: The Gathering
        - Système de gamification avec badges et XP
        - Profil utilisateur style carte MTG
        - PWA installable avec mode offline
        - Intégration MCP pour Claude Desktop
    """,
    'author': 'Nicolas JEUDY',
    'website': 'https://github.com/njeudy',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'assets': {
        'my_pwa_app.assets': [
            'my_pwa_app/static/dist/index.js',
            'my_pwa_app/static/dist/index.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}