# -*- coding: utf-8 -*-
{
	'name': 'Create Picking From SO Query',
	'version': '16.0.0.1.0',
	'license': 'LGPL-3',
	'author': "Fathoni Anwar",
	'sequence': 1,
	'website': 'https://rashadigital.com/',
	'category': 'Sale',
	'summary': '''Create Picking From SO using Stored Procedure With Condition :,
		If Commitment Date Delivery Greater Than Today,''',
	'depends': ['base','sale','stock'],
	'data': [
	'views/sale_order_sp_views.xml',
	],
	'installable': True,
	'application': True,
	'auto_install': False,
}