from odoo import models, api, fields


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    extra_amount = fields.Float(string='Extra Amount')
    extra_amount_journal_id = fields.Many2one('account.move', string="Extra Amount Journal")

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        if res.extra_amount > 0:
            journal = self.env['account.move'].create({
                'journal_id': 1, # Set the journal ID that you want to use
                'ref': 'Extra Amount',
                'line_ids': [(0, 0, {
                    'name': 'Extra Amount',
                    'account_id': res.partner_id.property_account_receivable_id.id, # Set the account ID that you want to use
                    'debit': res.extra_amount,
                    'credit': 0.0,
                }), (0, 0, {
                    'name': 'Extra Amount',
                    'account_id': self.env.company.extra_amount_account_id.id, # Set the account ID that you want to use
                    'debit': 0.0,
                    'credit': res.extra_amount,
                })],
            })
            res.write({'extra_amount_journal_id': journal.id})
        return res

    def button_cancel(self):
        for invoice in self:
            if invoice.extra_amount_journal_id:
                invoice.extra_amount_journal_id.unlink()
        return super(AccountInvoice, self).button_cancel()
