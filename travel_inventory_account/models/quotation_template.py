# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class QuotationTemplate(models.Model):
    _inherit = 'sale.order.template'

    inventory_account = fields.Many2one('account.account',)

