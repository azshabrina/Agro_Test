# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta , date
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from num2words import num2words
import logging
_logger = logging.getLogger(__name__)

class CompanyLanguage(models.Model):
   _inherit = "res.company"

   text_amount_language_currency = fields.Selection([('en', 'English'),
													 ('ar', 'Arabic'),
													 ('cz ', 'Czech'),
													 ('de', 'German'),
													 ('dk', 'Danish'),
													 ('en_GB', 'English - Great Britain'),
													 ('en_IN', 'English - India'),
													 ('es', 'Spanish'),
													 ('es_CO', 'Spanish - Colombia'),
													 ('es_VE', 'Spanish - Venezuela'),
													 ('eu', 'EURO'),
													 ('fi', 'Finnish'),
													 ('fr', 'French'),
													 ('fr_CH', 'French - Switzerland'),
													 ('fr_BE', 'French - Belgium'),
													 ('fr_DZ', 'French - Algeria'),
													 ('he', 'Hebrew'),
													 ('id', 'Indonesian'),
													 ('it', 'Italian'),
													 ('ja', 'Japanese'),
													 ('ko', 'Korean'),
													 ('lt', 'Lithuanian'),
													 ('lv', 'Latvian'),
													 ('no', 'Norwegian'),
													 ('pl', 'Polish'),
													 ('pt', 'Portuguese'),
													 ('pt_BR', 'Portuguese - Brazilian'),
													 ('sl', 'Slovene'),
													 ('sr', 'Serbian'),
													 ('ro', 'Romanian'),
													 ('ru', 'Russian'),
													 ('sl', 'Slovene'),
													 ('tr', 'Turkish'),
													 ('th', 'Thai'),
													 ('vi', 'Vietnamese'),
													 ('nl', 'Dutch'),
													 ('uk', 'Ukrainian'),
													 ], string='Text amount language/currency')

class AccountConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   text_amount_language_currency = fields.Selection(related="company_id.text_amount_language_currency",
													string='language_currency', readonly=False)
   @api.onchange('text_amount_language_currency')
   def save_text_amount_language_currency(self):
	   if self.text_amount_language_currency:
		   self.company_id.text_amount_language_currency = self.text_amount_language_currency

class AccountMoveKwitansi(models.Model):
	_inherit = 'account.move'

	text_amount = fields.Char(string="Total In Words", required=False, compute="amount_to_words" )

	@api.depends('amount_total')
	def amount_to_words(self):
	   if self.company_id.text_amount_language_currency:
		   self.text_amount = num2words(self.amount_total, to='currency',
										lang=self.company_id.text_amount_language_currency)

	def print_kwitansi(self):
		if self.payment_state == 'paid':
			return self.env.ref('agro_test_kuitansi.report_kwitansi_pdf').report_action(self)
		else:
			raise UserError(_("Print kwitansi pembayaran ini hanya untuk Invoice yang sudah lunas!"))