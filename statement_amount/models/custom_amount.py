# -*- coding: utf-8 -*-

from odoo import api, fields, models , _
from odoo.exceptions import UserError


class InheritAccountStatement(models.Model):
    _inherit = 'account.bank.statement'

    lines_amount = fields.Monetary(compute='_lines_amount')

    @api.depends('line_ids', 'balance_start', 'line_ids.amount', 'balance_end_real')
    def _lines_amount(self):
        for statement in self:
            statement.lines_amount = sum([line.amount for line in statement.line_ids])



