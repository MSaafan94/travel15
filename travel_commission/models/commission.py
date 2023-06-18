from odoo import fields, models, api


class ResponsibleCSTemplate(models.Model):
    _inherit = 'account.move'

    commission = fields.Integer()
