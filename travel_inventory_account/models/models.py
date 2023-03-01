# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InventoryAccountOrder(models.Model):
    _inherit = 'sale.order'

    inventory_account = fields.Many2one('account.account')

    @api.onchange('sale_order_template_id')
    def inventory_account_compute(self):
        self.inventory_account = self.sale_order_template_id.inventory_account



class InventoryAccount(models.Model):
    _inherit = 'sale.order.line'

    inventory_account = fields.Many2one('account.account',compute='inventory_account_compute')

    def inventory_account_compute(self):
        self.inventory_account = self.order_id.inventory_account

    def _prepare_invoice_line(self, **kwargs):
        res = super()._prepare_invoice_line(**kwargs)
        res.update({"account_id": self.inventory_account, })
        return res