from odoo import models, fields


class CustomCompanySettings(models.Model):
    _inherit = 'res.company'

    sales_manager = fields.Many2one('hr.employee', string='Sales Manager')
    cs_manager = fields.Many2one('hr.employee', string='Customer Service Manager')
    total_cs_commission = fields.Float(string='Total CS Commission')

class CustomAccountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_manager = fields.Many2one(
        related='company_id.sales_manager',
        string='Sales Manager',
        readonly=False,
    )
    cs_manager = fields.Many2one(
        related='company_id.cs_manager',
        string='Customer Service Manager',
        readonly=False,
    )
    total_cs_commission = fields.Float(
        related='company_id.total_cs_commission',
        string='Total CS Commission',
        readonly=False,
    )