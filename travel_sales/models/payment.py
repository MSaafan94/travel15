# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError, ValidationError
from copy import deepcopy
import logging
import time
from datetime import date
from collections import OrderedDict, defaultdict
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import formatLang, format_date
from odoo.tools import float_is_zero, float_compare
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp
from lxml import etree


class AccountPaymenttt(models.Model):
    _inherit = "account.payment"

    def post(self, invoice=False):
        if not self.env.user.has_group('account.group_account_manager') and (self.payment_type == 'inbound' or self.partner_type == 'customer'):
            raise UserError(_('please head to the accounting team to confirm it for you'))
        super(AccountPaymenttt, self).post()

