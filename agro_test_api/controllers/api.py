import json

from odoo import http
from odoo.http import request


class Api (http.Controller):

	@http.route(['/api/products'], type="http", auth="public", website=True, method=['GET'], csrf=False)
	def get_users(self):
		products_rec = request.env['product.template'].search([('active', '=', True)])
		if products_rec:
			products = []
			for product_data in products_rec:
				vals = {
					"name": str(product_data.name),
					"description": product_data.description,
					"default_code": product_data.default_code,
					"detailed_type": product_data.detailed_type,
					"categ_id": product_data.categ_id.name,
					"standard_price": product_data.standard_price,
					"list_price": product_data.list_price,
					"qty_available": product_data.qty_available,
					"uom_id": product_data.uom_id.name,
					"invoice_policy": str(product_data.invoice_policy),
				}
				products.append(vals)
			data = {
				'success': True,
				'data': {
					'total': len(products),
					'items': products
				}
			}
		else:
			data = {
				'error_code': 2000,
				'error_data': 'Products Not Found!'
			}
		return http.Response(
			json.dumps(data),
			status=200,
			mimetype='application/json'
		)