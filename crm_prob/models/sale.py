from odoo import models, fields, api

class SaleOrderr(models.Model):
    _inherit = 'sale.order'

    # is_duplicated = fields.Selection([('update', 'update'), ('confirmed', 'confirmed')])

    relationship_ids = fields.One2many('partner.relationship', 'relation_id', string='Relationships')

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.partner_id.name if record.partner_id else ''
    #         result.append((record.id, name))
    #     return result

    # @api.model
    # def create(self, vals):
    #     templates = super(SaleView, self).write(vals)
    #
    #     # fix attachment ownership
    #     for rec in self.relationship_ids:
    #         if rec.attachment_ids:
    #             rec.attachment_ids.write({'res_model': self._name, 'res_id': rec.id})
    #     return templates

    def action_cancel(self):
        # Call super to perform the cancellation of the sale order
        res = super(SaleOrderr, self).action_cancel()

        # Update opportunity stage to 'cancel' for related opportunities
        canceled_stage = self.env['crm.stage'].search([('name', '=', 'Canceled')], limit=1)
        for order in self:
            if order.opportunity_id:
                order.opportunity_id.stage_id = canceled_stage.id
        return res

    def action_confirm(self):
        res = super(SaleOrderr, self).action_confirm()

        won_stage = self.env['crm.stage'].search([('name', '=', 'won')], limit=1)

        for order in self:
            if order.opportunity_id:
                order.opportunity_id.stage_id = won_stage.id
        return res

