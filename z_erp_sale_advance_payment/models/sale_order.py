# -*- coding: utf-8 -*-
##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2022 Zone4Erp SSolutions (<zone4erp@gmail.com>).
#    For Module Support : zone4erp@gmail.com
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _advance_payment_count(self):
        for line in self:
            payment_ids = self.env['account.payment'].search([('sale_id', '=', line.id)])
            line.advance_payment_count = len(payment_ids)

    def advance_payment_button(self):
        self.ensure_one()
        return {
            'name': 'Advance Payment',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('sale_id', '=', self.id)],
        }

    advance_payment_count = fields.Integer(string='Advance Payment', compute='_advance_payment_count')

    def action_advance_payment(self):
        view_id = self.env['sale.advance.payment']
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Advance Payment Register',
            'res_model': 'sale.advance.payment',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': view_id.id,
            'view_id': self.env.ref('z_erp_sale_advance_payment.sale_order_advance_payment_register_wizard', False).id,
            'target': 'new',
            'context': {'default_partner_id': self.partner_id.id,
                        'default_company_id': self.company_id.id,
                        'default_amount': self.amount_total,
                        'default_memo': self.name,
                        'default_payment_type': 'inbound',
                        'default_partner_type': 'customer',
                        'default_currency_id': self.currency_id.id},
        }


class SaleAdvancePayment(models.TransientModel):
    _name = 'sale.advance.payment'

    partner_id = fields.Many2one('res.partner', 'Customer', required=1)
    company_id = fields.Many2one('res.company', 'Company', required=1)
    amount = fields.Monetary(string='Amount', required=True, tracking=True)
    payment_date = fields.Date(string='Date', default=fields.Date.context_today, required=True,
                               copy=False, tracking=True)
    journal_id = fields.Many2one('account.journal', 'Payment Journal', required=1)
    memo = fields.Char('Remarks / Memo', required=1)
    payment_type = fields.Selection([('outbound', 'Send Money'),
                                     ('inbound', 'Receive Money'),
                                     ('transfer', 'Internal Transfer')], string='Payment Type', required=True,
                                    )
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')], tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method')
    payment_method_code = fields.Char(related='payment_method_id.code', readonly=True)

    @api.onchange('journal_id')
    def _onchange_journal(self):
        if self.journal_id:
            if self.journal_id.currency_id:
                self.currency_id = self.journal_id.currency_id
            payment_methods = self.payment_type == 'inbound' and self.journal_id.inbound_payment_method_line_ids
            payment_methods_list = []
            for pm in payment_methods:
                payment_methods_list.append(pm.payment_method_id.id)

            default_payment_method_id = self.env.context.get('default_payment_method_id')
            if default_payment_method_id:
                payment_methods_list.append(default_payment_method_id)
            else:
                self.payment_method_id = payment_methods_list and payment_methods_list[0] or False
            domain = {'payment_method_id': [('id', 'in', payment_methods_list)]}
            return {'domain': domain}
        return {}

    def register_payment(self):
        rec_id = self._context.get('active_ids')[0]
        active_model = self._context.get('active_model')
        active_id = self.env[active_model].search([('id', '=', rec_id)], limit=1)
        payment = self.env['account.payment'].create({
            'date': self.payment_date,
            'payment_method_id': self.payment_method_id.id,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'amount': self.amount,
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'ref': self.memo + str(' - Advance Payment'),
            'sale_id': active_id.id,
        })
        return payment
        # if payment:
        #     payment.sudo().action_post()
