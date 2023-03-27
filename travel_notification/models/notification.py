from odoo import fields, models, api


class ResponsibleCSTemplate(models.Model):
    _inherit = 'sale.order.template'

    responsible_cs = fields.Many2one('res.users', string="responsible cs", track_visibility='always')


class ResponsibleCSOrder(models.Model):
    _inherit = 'sale.order'

    responsible_cs = fields.Many2one('res.users', string="responsible cs", track_visibility='always')
    lock_order = fields.Datetime(track_visibility='always')

    def action_done(self):
        super(ResponsibleCSOrder, self).action_done()
        self.lock_order = fields.Datetime.now()
        self.responsible_cs = self.sale_order_template_id.responsible_cs