from odoo import models, fields, api, _


class account_payment(models.Model):
    _inherit = "account.payment"

    sale_id = fields.Many2one('sale.order','Sales Order')
