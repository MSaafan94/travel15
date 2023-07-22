from odoo import models, fields, api, _
from odoo.exceptions import UserError


class purchase(models.Model):
    _inherit = 'purchase.order'
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    def apply_analytic_tags(self):
        if self.analytic_tag_ids or self.analytic_account_id:
            if self.order_line:  # assuming this is the field for line items in purchase order
                for line in self.order_line:
                    line.analytic_tag_ids |= self.analytic_tag_ids
                    if self.analytic_account_id:
                        line.account_analytic_id = self.analytic_account_id
            else:
                raise UserError(_("No Purchase Order Line items selected"))
        else:
            raise UserError(_("No Analytic Tags or Analytic Account Selected"))
