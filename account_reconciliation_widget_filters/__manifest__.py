# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account reconciliation widget filters',
    'version': '14.0.1.0.0',
    'summary': """
        Add Filters for available move line for bank reconciliation
    """,
    'description': """
    """,
    'author': 'Nicolas JEUDY (Alusage)',
    'website': 'https://nicolas.alusage.fr',
    'license': 'AGPL-3',
    'category': 'Technical',
    'depends': [
        'base',
        'account_reconciliation_widget',
    ],
    'data': [
        'views/account_account_view.xml',
    ],
    'demo': [],
    'auto_install': False,
    'external_dependencies': [],
    'application': False,
    'css': [],
    'images': [],
    'installable': True,
    'maintainer': 'Nicolas JEUDY',
    'pre_init_hook': '',
    'post_init_hook': '',
    'uninstall_hook': '',
}
