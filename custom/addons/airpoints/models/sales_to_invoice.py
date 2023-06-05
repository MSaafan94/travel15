from odoo import fields, models, api


class ExtraOrderFields(models.Model):
    _inherit = 'sale.order.line'

    name_ = fields.Char(string='name')
    trip_code = fields.Char()
    airline = fields.Char()
    serial_number = fields.Char()
    route = fields.Char()
    tkt_no = fields.Char()
    reference = fields.Char()
    cost = fields.Char()

    def _prepare_invoice_line(self, **optional_values):

        res = super(ExtraOrderFields, self)._prepare_invoice_line(**optional_values)
        res.update({
            'name_': self.name_,
            'trip_code': self.trip_code,
            'airline': self.airline,
            'serial_number': self.serial_number,
            'route': self.route,
            'tkt_no': self.tkt_no,
            'reference': self.reference,
            'cost': self.cost,
        })
        return res


class AccountInvoiceLineExtraFields(models.Model):
    _inherit = "account.move.line"

    name_ = fields.Char()
    trip_code = fields.Char()
    airline = fields.Char()
    serial_number = fields.Char()
    route = fields.Char()
    tkt_no = fields.Char()
    reference = fields.Char()
    cost = fields.Char()