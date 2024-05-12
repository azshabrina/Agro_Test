# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta , date
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import logging
_logger = logging.getLogger(__name__)

class SaleOrderPicking(models.Model):
	_inherit = 'sale.order'


	@api.model
	def init(self):
		_logger.info("creating confirm_sales_order function...")
		self.env.cr.execute("""CREATE OR REPLACE PROCEDURE public.confirm_sales_order(
				v_so_id INT, v_origin text, v_partner_id INT, v_picking_type_id INT, v_company_id INT, v_warehouse_id INT, v_location_id INT, v_location_dest_id INT, v_move_type text, v_state text, v_procure_method text)

			AS $BODY$
			DECLARE
				x_proc_group INT;
				x_seq_no text;
			BEGIN
				-- Insert into the procurement_group table
				INSERT INTO procurement_group (partner_id, name, move_type, sale_id)
				SELECT partner_id, name, picking_policy, id
				FROM sale_order
				LIMIT 1
				RETURNING id INTO x_proc_group;
				
				-- Check last Sequence picking number
				SELECT
				concat('WH/OUT/',to_char(last_value+1, '00000'))::text
				INTO x_seq_no 
				FROM stock_picking_id_seq
				WHERE is_called = true;

				-- Create stock picking & stock move
				WITH picking as (
				  INSERT INTO stock_picking(partner_id, picking_type_id, location_id, location_dest_id, move_type, state, company_id, origin, group_id, sale_id, name)
				  VALUEs(v_partner_id, v_picking_type_id, v_location_id, v_location_dest_id, v_move_type, v_state, v_company_id, v_origin, x_proc_group, v_so_id, x_seq_no)
				  RETURNING id, location_id, location_dest_id, group_id, picking_type_id, state, origin, partner_id, company_id, scheduled_date
				)
				INSERT INTO stock_move(picking_id,location_id,location_dest_id, group_id, picking_type_id, state, origin, partner_id, company_id, product_id, product_uom, 
							product_qty, product_uom_qty, sale_line_id, name, procure_method, date)
				  SELECT s1.id, s1.location_id, s1.location_dest_id, s1.group_id, s1.picking_type_id, s1.state, s1.origin, s1.partner_id, s1.company_id, s2.product_id, s2.product_uom, 
							s2.product_uom_qty, s2.product_uom_qty, s2.id, s2.name, 'make_to_stock', s2.write_date
				  FROM picking s1
				  INNER JOIN sale_order_line s2 ON s2.order_id = v_so_id;

				-- Update Sales Order & Sales order line				
				UPDATE sale_order 
				SET 
				procurement_group_id = x_proc_group,
				state = 'sale'
				WHERE id = v_so_id;

				UPDATE sale_order_line 
				SET 
				state = 'sale',
				qty_to_invoice = qty_delivered
				WHERE order_id = v_so_id;

			END;
			$BODY$
			LANGUAGE PLPGSQL;
		""")

	def confirm_sales_order(self):
		if self.picking_policy == 'direct':
			origin = self.name
			partner_id = self.partner_id.id
			picking_type_id = self.warehouse_id.out_type_id.id
			company_id = self.company_id.id
			warehouse_id = self.warehouse_id.id
			location_id = self.warehouse_id.lot_stock_id.id
			location_dest_id = self.partner_id.property_stock_customer.id
			# expected_date = self.expected_date.date()
			move_type = self.picking_policy
			state = 'confirmed'
			procure_method = 'make_to_stock'
			self.env.cr.execute("CALL confirm_sales_order(%s, '%s', %s, %s, %s, %s, %s, %s, '%s', '%s', '%s')" 
				% (self.id,origin,partner_id,picking_type_id,company_id,warehouse_id,location_id,location_dest_id,move_type,state,procure_method))
		else:
			raise UserError(_("Konfirmasi Order hanya di peruntukan untuk Order dengan Shipping Policy : As soon as possible [direct]"))