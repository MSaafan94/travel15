# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InvoiceInherit(models.Model):
    _inherit = 'account.move'

    payment_typee = fields.Many2one('account.journal',)
    so = fields.Many2one('sale.order')

    def action_register_payment(self):
        res = super().action_register_payment()
        if self.is_invoice(include_receipts=True):
            # Pass custom field values to the payment wizard
            res['context'].update({
                'default_so': self.so.id,
                'default_trip_reference': self.sale_order_template_id.id,
            })
        return res

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    so = fields.Many2one('sale.order', string='SO')
    trip_reference = fields.Many2one('sale.order.template', string='Trip_reference')

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        activity_type_id = self.env.ref('mail.mail_activity_data_todo').id
        if self.trip_reference and self.trip_reference.responsible_cs:
            user_id = self.trip_reference.responsible_cs.id
            activity_vals = {
                'activity_type_id': activity_type_id,
                'res_id': self.id,
                'res_model_id': self.env.ref('account.model_account_payment').id,
                'user_id': user_id,
                'date_deadline': fields.Date.today(),
                'summary': 'Payment posted',
                'note': 'Payment %s has been posted' % self.id,
            }
            self.env['mail.activity'].create(activity_vals)

        # Add custom field values to the payment
        payment_vals.update({
            'sale_id': self.so.id,
            'trip_reference': self.trip_reference.id,
        })
        return payment_vals


class AdvancePayment(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):

        invoice = super()._prepare_invoice()
        invoice.update({'so': self.id,'sale_order_template_id': self.sale_order_template_id})
        return invoice

    def action_down_payment(self):
        view_id = self.env['sale.advance.payment.inv']
        return {
            'type': 'ir.actions.act_window',
            'name': 'Down payment',
            'res_model': 'sale.advance.payment.inv',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': view_id.id,
            'view_id': self.env.ref('sales_extra_fields.downpayment_wizard_form', False).id,
            'target': 'new',
        }


class DownpaymentWizard(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    fixed_amount = fields.Float(string="Fixed Amount", required=True)
    payment_typee = fields.Many2one('account.journal',)



    @api.model
    def _create_invoice(self, order, so_line, amount):
        # Call the original method to create the invoice
        invoice = super(DownpaymentWizard, self)._create_invoice(order, so_line, amount)

        # Update the invoice with the payment_type value
        invoice.write({'payment_typee': self.payment_typee.id})

        return invoice

    def create_invoicess(self, advance_payment_method=None, fixed_amount=None):
            sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
            self.advance_payment_method = 'fixed'

            if self.advance_payment_method == 'delivered':
                sale_orders._create_invoices(final=self.deduct_down_payments)
            else:
                # Create deposit product if necessary
                if not self.product_id:
                    vals = self._prepare_deposit_product()
                    self.product_id = self.env['product.product'].create(vals)
                    self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id',
                                                                     self.product_id.id)

                sale_line_obj = self.env['sale.order.line']
                for order in sale_orders:
                    amount, name = self._get_advance_details(order)

                    if self.product_id.invoice_policy != 'order':
                        raise UserError(
                            _('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                    if self.product_id.type != 'service':
                        raise UserError(
                            _("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                    taxes = self.product_id.taxes_id.filtered(
                        lambda r: not order.company_id or r.company_id == order.company_id)
                    tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                    analytic_tag_ids = []
                    for line in order.order_line:
                        analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                    so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                    so_line = sale_line_obj.create(so_line_values)
                    self._create_invoice(order, so_line, amount)
            if self._context.get('open_invoices', False):
                return sale_orders.action_view_invoice()
            return {'type': 'ir.actions.act_window_close'}

    def _prepare_invoice_values(self, order, name, amount, so_line):
        # Call the super method to get the original dictionary
        invoice_values = super(DownpaymentWizard, self)._prepare_invoice_values(order, name, amount, so_line)

        # Add your custom fields to the dictionary
        invoice_values.update({
            'so': order.id,
            'sale_order_template_id': order.sale_order_template_id
        })

        # Return the updated dictionary
        return invoice_values


