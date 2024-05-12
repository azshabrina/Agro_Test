# -*- coding: utf-8 -*-
{
	'name': 'Custom Dashboard Sales & Purchase Order',
	'version': '16.0.0.1.0',
	'license': 'LGPL-3',
	'author': "Fathoni Anwar",
	'sequence': 1,
	'website': 'https://rashadigital.com/',
	'category': 'Dashboard',
	'summary': '''Custom Dashboard For Sales & Purchase Order''',
	'depends': ['web','sale','purchase'],
	'data': [
	'views/dashboard_views.xml',
	],
	'assets': {
	'web.assets_backend': [
	   '/agro_test_dashboard/static/src/js/dashboard_action.js',
	   '/agro_test_dashboard/static/src/xml/dashboard.xml',
	   '/agro_test_dashboard/static/src/css/dashboard.css',
   ],
   },
	'installable': True,
	'application': True,
	'auto_install': False,
}