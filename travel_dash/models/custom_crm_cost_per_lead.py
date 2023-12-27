from odoo import models, fields, api

class LeadCost(models.Model):
    _name = 'custom_crm_cost_per_lead.lead_cost'
    _description = 'Lead Cost'

    lead_id = fields.Many2one('crm.lead', string='Lead')
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    cost_per_lead = fields.Float(string='Cost per Lead')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    @api.depends('date')
    def _compute_month(self):
        for record in self:
            if record.date:
                record.month = record.date.strftime('%Y-%m')

    month = fields.Char(string='Month', compute='_compute_month', store=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('template_id')
    def onchange_template_id(self):
        """
        Override the onchange method for the quotation template to prevent
        the removal of order lines when changing the template.
        """
        if self.order_line and self.template_id:
            # Preserve existing order lines
            existing_order_lines = self.order_line
            self.order_line = False  # Clear existing order lines

            # Apply the new template
            super(SaleOrder, self).onchange_template_id()

            # Restore the existing order lines
            self.order_line += existing_order_lines

        else:
            # Default behavior if no existing order lines
            super(SaleOrder, self).onchange_template_id()

