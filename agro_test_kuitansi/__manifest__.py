# -*- coding: utf-8 -*-
{
    'name': 'Printout Kwitansi',
    'version': '16.0.0.1.0',
    'license': 'LGPL-3',
    'author': "Fathoni Anwar",
    'sequence': 1,
    'website': 'https://rashadigital.com/',
    'category': 'Accounting',
    'summary': 'Printout Kwintansi Lunas',
    'depends': ['base','account'],
    'data': [
        'report/report_view.xml',
        'views/account_move_views.xml',
     ],
    'installable': True,
    'application': True,
    'auto_install': False,
}