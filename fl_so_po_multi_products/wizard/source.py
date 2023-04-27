from odoo import api, fields, models

class AccountMovee(models.Model):
    _inherit = 'account.move'

    source_document = fields.Char(string='Source Document')

    @api.model
    def default_get(self, fields):
        """Override default_get to set default values."""
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')
        if active_model == 'purchase.order' and active_ids:
            source_document = self.env[active_model].browse(active_ids).name
            res.update({'source_document': source_document})
        elif active_model == 'sale.order' and active_ids:
            source_document = self.env[active_model].browse(active_ids).name
            res.update({'source_document': source_document})
        return res