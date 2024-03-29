from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_purchase_order(self):
        self.ensure_one()
        action = self._get_purchase_rfq_action()
        action['domain'] = [('origin', '=', self.name)]
        return action

    def _get_purchase_rfq_action(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'name': 'Request for Quotation',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def _get_po(self):
        for orders in self:
            purchase_ids =self.env['purchase.order'].search([('origin', '=', self.name)])
        orders.po_count = len(purchase_ids)

    po_count = fields.Integer(compute='_get_po', string='Purchase Orders')