# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api


class SelectProducts(models.TransientModel):

    _name = 'select.products'
    _description = 'Select Products'

    product_ids = fields.Many2many('product.product', string='Products')
    flag_order = fields.Char('Flag Order')

    def select_products(self):
        if self.flag_order == 'so':
            order_id = self.env['sale.order'].browse(self._context.get('active_id', False))
            for product in self.product_ids:
                self.env['sale.order.line'].create({
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'price_unit': product.lst_price,
                    'order_id': order_id.id
                })
        elif self.flag_order == 'po':
            order_id = self.env['purchase.order'].browse(self._context.get('active_id', False))
            for product in self.product_ids:
                self.env['purchase.order.line'].create({
                    'product_id': product.id,
                    'name': product.name,
                    'date_planned': order_id.date_planned or datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'product_uom': product.uom_id.id,
                    'price_unit': product.lst_price,
                    'product_qty': 1.0,
                    'display_type': False,
                    'order_id': order_id.id
                })
        elif self.flag_order == 'opt':  # New condition for optional product tab in quotation template
            template_id = self.env['sale.order.template'].browse(self._context.get('active_id', False))
            for product in self.product_ids:
                self.env['sale.order.template.option'].create({
                    'name': product.name,
                    'product_id': product.id,
                    'uom_id': product.uom_id.id,
                    'price_unit': product.lst_price,
                    'sale_order_template_id': template_id.id
                })