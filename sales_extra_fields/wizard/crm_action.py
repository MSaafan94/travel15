from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PaymentWizards(models.TransientModel):
    _name = 'crm.wizard'
    # _description = 'Description'
    source = fields.Many2one('utm.source', "Source",)
    lead_source = fields.Many2one('utm.source', "lead_Source",)
    destination = fields.Many2one('destination', 'Destination')
    service_type = fields.Many2one('service.type', 'service type')

    def set_fields(self):
        model = self.env.context.get('active_model')
        crm_ids = self.env[model].browse(self.env.context.get('active_ids'))
        for lead in crm_ids:
            if self.source:
                lead.source_id = self.source.id
            if self.destination:
                lead.destination_1 = self.destination
            if self.lead_source:
                lead.lead_source = self.lead_source
            if self.service_type:
                lead.service_type = self.service_type


class CRMLead(models.Model):
    _inherit = "crm.lead"

    def set_field_wizard(self):
        ctx = self.env.context
        return {
            'type': 'ir.actions.act_window',
            'name': 'Set fields',
            'res_model': 'crm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sales_extra_fields.set_fields_form', False).id,
            'target': 'new',
            'context': ctx
        }
