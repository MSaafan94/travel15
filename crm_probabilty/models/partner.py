from odoo import models, fields, api


class PartnerStatus(models.Model):
    _inherit = 'res.partner'

    customer_status = fields.Selection([])
