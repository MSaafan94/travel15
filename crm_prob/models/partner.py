from odoo import models, fields, api


class PartnerStatus(models.Model):
    _inherit = 'res.partner'

    acquisition_lead = fields.Many2one('utm.source')
    customer_status = fields.Selection([('active', 'Active'), ('disqualified', 'Disqualified')], default="active")
    profession = fields.Many2one('pro.profession')
    education = fields.Many2one('edu.education')
    region = fields.Many2one('reg.region')
