from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        invoice_vals.update({
            'individual': self.individual,
            'adult': self.adult,
            'child': self.child,
            'infant': self.infant,
            'salesperson': self.user_id,
            'final_invoice': True,
        })
        return invoice_vals


class CustomCompanySettings(models.Model):
    _inherit = 'res.company'

    sales_manager = fields.Many2one('res.users', string='Sales Manager')
    cs_manager = fields.Many2one('res.users', string='Customer Service Manager')
    cs_persons = fields.Many2many('res.users', string='Customer Service Manager')
    total_cs_commission = fields.Float(string='Total CS Commission')
    cs_person_share = fields.Float()
    cs_manager_share = fields.Float()
