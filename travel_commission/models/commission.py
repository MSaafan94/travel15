from odoo import models, fields, api


class CustomUserFields(models.Model):
    _inherit = 'res.users'

    analytic_account = fields.Many2one('account.analytic.account', )
    analytic_tag = fields.Many2many('account.analytic.tag', )


class AccountMove(models.Model):
    _inherit = 'account.move'

    adult = fields.Integer(string='Adult')
    child = fields.Integer(string='Child')
    infant = fields.Integer(string='Infant')
    down_payment = fields.Boolean()
    final_invoice = fields.Boolean()
    agent_commission_percent = fields.Float(string='Agent Commission %', default=5.0)
    extra_journal_entries = fields.One2many('account.move', 'source_invoice_id', string='Extra Journal Entries')
    source_invoice_id = fields.Many2one('account.move', string='Source Invoice', ondelete='cascade')

    price_adult = 300
    price_child = 200
    price_infant = 100

    individual = fields.Selection(
        [('individual', 'Individual'), ('visa', 'Visa'), ('group', 'Group')],
        string="Branch"
    )
    salesperson = fields.Many2one('res.users')
    cs_persons = fields.Many2many('res.users')

    def action_post(self):
        res = super().action_post()

        for move in self:
            move._create_journal_entry()
        return res

    def action_invoice_cancel(self):
        # Call the original action_invoice_cancel method
        res = super().action_invoice_cancel()

        # Cancel the associated journal entry
        for move in self:
            if move.source_invoice_id:
                move.button_draft()
                move.unlink()

        return res

    def action_draft(self):
        # Call the original action_draft method
        res = super().action_draft()

        # Set the associated journal entry to draft
        for move in self:
            associated_entry = self.env['account.move'].search([('source_invoice_id', '=', move.id)], limit=1)
            if associated_entry:
                associated_entry.button_draft()

        return res

    def _create_journal_entry(self):
        # Do not create an extra journal entry if the source_invoice_id field is already set
        price_adult_sales_person = 300
        price_child_sales_person = 200
        price_infant_sales_person = 100

        price_sales_manager = 100

        num_salespeople = len(self.company_id.cs_persons)

        # Calculate the total amount based on the number of adults, children, and infants
        total_amount_sales_person = (self.adult * price_adult_sales_person) + (
                    self.child * price_child_sales_person) + (self.infant * price_infant_sales_person)
        total_amount_sales_manager = (self.adult * price_sales_manager) + (self.child * price_sales_manager)
        total_amount_cs_person = (self.adult * self.company_id.cs_person_share) + (
                    self.child * self.company_id.cs_person_share)
        total_amount_cs_manager = (self.adult * self.company_id.cs_manager_share) + (
                    self.child * self.company_id.cs_manager_share)

        if self.source_invoice_id:
            return

        journal = self.env['account.journal'].search([('name', '=', 'Miscellaneous Operations')], limit=1)
        company_id = self.env.user.company_id.id
        if not journal:
            # Create the journal if it doesn't exist
            journal = self.env['account.journal'].create({
                'name': 'Miscellaneous Operations',
                'code': 'MISC',
                'type': 'general',  # Keep the journal type as 'general'
                'company_id': company_id,
            })

        account_payable = self.env['account.account'].search([('code', '=', '2280004')], limit=1)
        account_com = self.env['account.account'].search([('code', '=', '3210029')], limit=1)

        cs_person_lines = []
        cs_person_debit = num_salespeople * total_amount_cs_person

        if journal and account_payable and account_com and self.final_invoice and self.individual=='group':
            move = self.env['account.move'].create({
                'journal_id': journal.id,
                'date': fields.Date.today(),
                'ref': self.name,
                'move_type': 'entry',  # Set move_type to 'entry' for general journal entries
                'source_invoice_id': self.id,  # Set the source_invoice_id to the current move's ID
            })
            for cs_person in self.company_id.cs_persons:
                cs_person_lines.append(
                    (0, 0, {
                        'account_id': account_com.id,
                        'debit': total_amount_cs_person,
                        'name': 'cs persons',
                        'credit': 0,
                        'move_id': move.id,
                        'analytic_account_id': cs_person.analytic_account.id,
                        'analytic_tag_ids': [(6, 0, cs_person.analytic_tag.mapped('id'))],
                    })
                )

            move_line_vals = [
                (0, 0, {
                    'account_id': account_com.id,
                    'debit': total_amount_sales_manager,
                    'credit': 0,
                    'name': 'sales_manager',
                    'move_id': move.id,
                    'analytic_account_id': self.company_id.sales_manager.analytic_account.id,
                    'analytic_tag_ids': [(6, 0, self.company_id.sales_manager.analytic_tag.mapped('id'))],

                }),
                (0, 0, {
                    'account_id': account_com.id,
                    'debit': total_amount_sales_person,
                    'credit': 0,
                    'name': 'sales person',
                    'move_id': move.id,
                    'analytic_account_id': self.salesperson.analytic_account.id,
                    'analytic_tag_ids': [(6, 0, self.salesperson.analytic_tag.mapped('id'))],

                }),
                (0, 0, {
                    'account_id': account_com.id,
                    'debit': total_amount_cs_manager,
                    'name': 'cs manager',
                    'credit': 0,
                    'move_id': move.id,
                    'analytic_account_id': self.company_id.cs_manager.analytic_account.id,
                    'analytic_tag_ids': [(6, 0, self.company_id.cs_manager.analytic_tag.mapped('id'))],

                }),
                *cs_person_lines,
                (0, 0, {
                    'account_id': account_payable.id,
                    'debit': 0,
                    'credit': total_amount_sales_person + total_amount_sales_manager + total_amount_cs_manager + cs_person_debit,
                    'move_id': move.id,
                }),
            ]

            move.write({'line_ids': move_line_vals})
            move.action_post()
