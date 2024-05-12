from odoo import models, api

class SaleDashboard(models.Model):
   _inherit = 'sale.order'

   @api.model
   def get_data(self):
	   all_order = self.env['sale.order'].search([('state', 'in', ['sale','done'])])
	   total_order_amount = sum(all_order.mapped('amount_total'))
	   all_quotation = self.env['sale.order'].search([('state', 'not in', ['sale','done','cancel'])])
	   customers = self.env['res.partner'].search([('customer_rank', '=', 1)])
	   return {
		   'total_order': len(all_order),
		   'total_order_amount': total_order_amount,
		   'total_quotation': len(all_quotation),
		   'total_customer': len(customers),
	   }

class PurchaseDashboard(models.Model):
   _inherit = 'purchase.order'

   @api.model
   def get_data(self):
	   all_order = self.env['purchase.order'].search([('state', 'in', ['purchase','done'])])
	   total_order_amount = sum(all_order.mapped('amount_total'))
	   priority = self.env['purchase.order'].search([('priority', '=', '1')])
	   supplier = self.env['res.partner'].search([('supplier_rank', '=', 1)])
	   return {
		   'total_purchase': len(all_order),
		   'total_purchase_amount': total_order_amount,
		   'total_priority': len(priority),
		   'total_supplier': len(supplier),
	   }