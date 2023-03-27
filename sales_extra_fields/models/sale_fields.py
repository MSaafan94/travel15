# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Destination(models.Model):
    _name = 'model.destination'
    _description = "Destination"

    _rec_name = 'destination'
    destination = fields.Char('Destination', help='Destination')


class Hotel(models.Model):
    _name = 'model.hotel'
    _description = "Hotel"

    _rec_name = 'hotel'
    hotel = fields.Char('Hotel', help='Hotel')


class AccountInvoice(models.Model):
    _inherit = 'account.move'
    sale_order_template_id = fields.Many2one('sale.order.template', string='Trip Reference')
    active = fields.Boolean(default=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    description = "Sale Order"

    sale_order_template_id = fields.Many2one('sale.order.template', string='Trip Reference', track_visibility='always')
    total_num = fields.Integer(compute='total_name_of_persons')
    # purchase = fields.Integer(compute='_purchase', string='Purchase', copy=False)
    res = fields.Many2one('res.partner', track_visibility='always')
    partner_age = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)


    def generate(self):
        months = {
            '1': 'JAN',
            '2': 'FEB',
            '3': 'MAR',
            '4': 'APR',
            '5': 'MAY',
            '6': 'JUN',
            '7': 'JUL',
            '8': 'AUG',
            '9': 'SEPT',
            '10': 'OCT',
            '11': 'NOV',
            '12': 'DEC',
        }
        if self.analytic_account_id:
            raise UserError(_("Analytic account already has value"))
        month = months.get(self.month)
        year = self.sale_order_template_id.name
        if not month and not self.sale_order_template_id:
            raise UserError(_("Month or trip reference not assigned in quotation template"))

        search_analytics = self.env['account.analytic.account'].search(
            [('name', 'like', '{}/{}'.format(month, year[-2:]))])
        group = self.env['account.analytic.group'].search([('name', '=', 'Individual Trips')], limit=1),
        serial = '0001'
        if search_analytics:
            serial = search_analytics[len(search_analytics) - 1].name.partition('/')[0]
            if serial:
                if int(serial) < 9:
                    serial = '000{}'.format(int(serial) + 1)
                elif int(serial) < 99:
                    serial = '00{}'.format(int(serial) + 1)
                elif int(serial) < 1000:
                    serial = '0{}'.format(int(serial) + 1)
                else:
                    serial = '{}'.format(int(serial) + 1)

        values = {
            'name': '{}/{}/{}'.format(serial, month, year[-2:]),
            'partner_id': self.partner_id.id,
            'group_id': group[0].id,
            # 'code': self.name
        }
        self.env['account.analytic.account'].sudo().create(values)
        self.analytic_account_id = self.env['account.analytic.account'].search(
            [('name', '=', '{}/{}/{}'.format(serial, month, year[-2:])), ('partner_id', '=', self.partner_id.name)],
            limit=1)

    def get_partner(self):
        # print(self.partner_id.age_type)
        self.partner_age = self.partner_id.age_type

    # def _purchase(self):
    #     self.ensure_one()
    #     for payment in self:
    #         payment.purchase = self.env['purchase.order'].search_count(
    #             [('origin', '=', self.name)])
    #
    # def purchase_action(self):
    #     action = self.env['ir.actions.act_window'].for_xml_id('purchase', 'purchase_rfq')
    #     action['domain'] = [('origin', '=', self.name), ]
    #     return action

    @api.onchange('name_of_persons')
    def total_name_of_persons(self):
        self.total_num = len(self.name_of_persons) + 1

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if self.sale_order_template_id:
            vals['sale_order_template_id'] = self.sale_order_template_id.id
        return vals

    state = fields.Selection([
        ('draft', 'Initial Booking'),
        ('waiting', 'Waiting List'),
        ('sent', 'Quotation Sent'),
        ('update', 'Update'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('expired', 'Expired'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')

    month = fields.Selection(related="sale_order_template_id.month", store=True)

    cancellation_policy = fields.Boolean(track_visibility='always')
    destination = fields.Many2one('model.destination', string="Hotel", track_visibility='always')
    # hotel = fields.Many2many('model.hotel', string="Hotel")
    duration = fields.Integer('Duration', track_visibility='always')
    hotel = fields.Many2many("model.hotel", string='Hotel', track_visibility='always')
    starttime = fields.Date(string='Order Date', required=True, index=True, default=fields.Datetime.now,
                                track_visibility='always')
    endtime = fields.Date(string='Order Date', required=True, index=True, default=fields.Datetime.now,
                              track_visibility='always')
    need_room_mate = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')], string="Need Room Mate", default='yes', track_visibility='always')
    no_of_accompanying_persons = fields.Integer("No of Accompanying Persons", track_visibility='always')
    # name_of_persons = fields.Many2many('res.partner',domain="[('is_company','=',True)]")
    #         domain="[('group','=', promotion_group)]",

    name_of_persons = fields.Many2many('res.partner', domain="[('parent_id', '=', partner_id)]",
                                       track_visibility='always')
    attachment_ids = fields.One2many('sale.attachments', 'sale_id', "Attachments", track_visibility='always')
    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account", track_visibility='always')
    cut_of_date = fields.Date(related='sale_order_template_id.cut_of_date', track_visibility='always')
    roommate_name = fields.Many2one('res.partner', 'Room Mate Name', track_visibility='always')

    adult = fields.Integer(  track_visibility='always')
    child = fields.Integer(  track_visibility='always')
    infant = fields.Integer(  track_visibility='always')

    # adultt = fields.Integer(related="adult", store=True)
    # childd = fields.Integer(related="child", store=True)
    # infantt = fields.Integer(related="infant", store=True)

    # @api.one
    @api.onchange('name_of_persons', 'partner_id', 'partner_age')
    def calculate_adult_child(self):
        self.ensure_one()
        # if not self.individual:
        if self.partner_id.age_type == 'infant':
            self.infant += 1
        elif self.partner_id.age_type == 'child':
            self.child += 1
        elif self.partner_id.age_type == 'adult':
            self.adult += 1
        for rec in self.name_of_persons:
            if rec.birthday:
                total_days = self.endtime - rec.birthday
                years = abs(total_days.days / 365)
                remaining_days = total_days.days % 365
                if remaining_days >= 30:
                    months = abs(remaining_days / 30)
                else:
                    months = 0
                if (remaining_days % 30) < 30:
                    days = (remaining_days % 30)
                else:
                    days = 0
                rec.years = years
                rec.months = months
                rec.days = days
                if 0 <= years < 2:
                    rec.age_type = 'infant'
                elif 2 <= years < 12:
                    rec.age_type = 'child'
                else:
                    rec.age_type = 'adult'

                if rec.age_type == 'infant':
                    self.infant += 1
                if rec.age_type == 'child':
                    self.child += 1
                if rec.age_type == 'adult':
                    self.adult += 1

    # @api.one
    @api.depends('name_of_persons')
    def _get_count_age_type(self):
        if self.name_of_persons:
            for rec in self.name_of_persons:
                if rec.age_type == 'infant':
                    self.infant += 1
                if rec.age_type == 'child':
                    self.child += 1
                if rec.age_type == 'adult':
                    self.adult += 1
        else:
            self.infant = 0
            self.child = 0
            self.adult = 0

        if self.partner_id.age_type == 'infant':
            self.infant += 1
        elif self.partner_id.age_type == 'child':
            self.child += 1
        elif self.partner_id.age_type == 'adult':
            self.adult += 1

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id)

    def action_waiting_list(self):
        self.state = 'waiting'

    # #@api.multi
    # @api.onchange('partner_id')
    # def get_name_of_persons(self):
    #     for rec in self:
    #         if rec.partner_id:
    #             current_partner_ids = rec.partner_id.child_ids.ids
    #             rec.name_of_persons = False
    #             return {
    #                 'domain': {
    #                     'name_of_persons': [('id', 'in', current_partner_ids)]
    #                 }
    #             }

    # #@api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        child_ids = self.partner_id.child_ids.ids
        self.name_of_persons = None
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'user_id': self.partner_id.user_id.id or self.partner_id.commercial_partner_id.user_id.id or self.env.uid,
            'name_of_persons': [(4, x) for x in child_ids]
        }
        if self.env['ir.config_parameter'].sudo().get_param(
                'sale.use_sale_note') and self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)

    @api.onchange('starttime', 'endtime')
    def get_duration(self):
        d1 = self.starttime
        d2 = self.endtime
        self.duration = abs((d2 - d1).days)


    # # #@api.multi
    # # @api.onchange('sale_order_template_id')
    # # def get_pricelist_from_quotaion(self):
    # #     if self.sale_order_template_id:
    # #         self.pricelist_id = self.sale_order_template_id.pricelist_id.id


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # cost = fields.Float('Cost',related="product_id.standard_price",readonly=False)
    selling = fields.Float('Selling')


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"
    _description = "Quotation Template"

    destination = fields.Many2one('model.destination', string="Hotel", track_visibility="always")
    # hotel = fields.Many2many('model.hotel', string="Hotel")
    duration = fields.Integer('Duration', readonly=True, store=True, track_visibility="always")
    hotel = fields.Many2many("model.hotel", string='Hotel', track_visibility="always")
    starttime = fields.Date(string='Order Date', required=True, index=True, default=fields.Datetime.now,
                                track_visibility="always")
    endtime = fields.Date(string='Order Date', required=True, index=True, default=fields.Datetime.now,
                              track_visibility="always")
    need_room_mate = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')], string="Need Room Mate", default='yes', track_visibility="always")
    no_of_accompanying_persons = fields.Integer("No of Accompanying Persons", track_visibility="always")
    name_of_persons = fields.Text("Names of Persons", track_visibility="always")
    attachment_ids = fields.One2many('quotation.attachments', 'quo_tem_id', "Attachments", track_visibility="always")
    pricelist_id = fields.Many2one('product.pricelist', "Pricelist", track_visibility="always")
    warehouse_id = fields.Many2one('stock.warehouse', "Warehouse", track_visibility="always")
    arranged = fields.Boolean(string="Arranged", track_visibility="always")
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', "November"),
        ('12', 'December'),
    ], 'Month', store=True, track_visibility="always"
    )
    year = fields.Selection([('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default='2023',
                            track_visibility="always")
    individual = fields.Boolean(string='Individual', track_visibility="always")
    cut_of_date = fields.Date('Cut Of Date', track_visibility="always")
    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account", track_visibility="always")
    analytic_tag_ids = fields.Many2one('account.analytic.tag', 'Analytic Tags', track_visibility="always")

    @api.onchange('endtime')
    def get_duration(self):
        d1 = self.starttime
        d2 = self.endtime
        self.duration = abs((d2 - d1).days)

    # #@api.multi
    def apply_analytic_tags(self):
        self.ensure_one()
        if self.analytic_tag_ids:
            if self.sale_order_template_option_id:
                for option_product in self.sale_order_template_option_id:
                    option_product.analytic_tag_ids = self.analytic_tag_ids.id
            else:
                raise UserError(_("No Optional products Selected"))
        else:
            raise UserError(_("No Analytic Tags Selected"))


class VechicleType(models.Model):
    _name = 'vehicle.type'

    name = fields.Char("Name", required=1)


class notess(models.Model):
    _name = 'notes.notes'

    name = fields.Char("Name", required=1)


class RoomNumber(models.Model):
    _name = 'room.number'

    name = fields.Char("Name", required=1)
    view = fields.Char(string='View', required=1)


class RoomView(models.Model):
    _name = 'room.view'

    name = fields.Char("Name", required=1)


class RoomSpecial(models.Model):
    _name = 'room.special'

    name = fields.Char("Name", required=1)


class MealPlan(models.Model):
    _name = 'meal.plan'

    name = fields.Char("Name", required=1)


class RoomType(models.Model):
    _name = 'room.type'

    name = fields.Char("Name", required=1)


class Flight(models.Model):
    _name = 'flight'

    name = fields.Char("Name", required=1)


class SpecialRequests(models.Model):
    _name = 'special.requests'

    name = fields.Char("Name", required=1)


class Program(models.Model):
    _name = 'program'

    name = fields.Char("Name", required=1)


class AddProgram(models.Model):
    _name = 'add.program'

    name = fields.Char("Name", required=1)


class Vaccination(models.Model):
    _name = 'vaccination'

    name = fields.Char("Name", required=1)


class VisaType(models.Model):
    _name = 'visa.type'

    name = fields.Char("Name", required=1)


class Responsibility(models.Model):
    _name = 'responsibility'

    name = fields.Char("Name", required=1)


class VisaSituation(models.Model):
    _name = 'visa.situation'

    name = fields.Char("Name", required=1)


class QuotationAttachments(models.Model):
    _name = 'quotation.attachments'

    quo_tem_id = fields.Many2one('sale.order.template')
    attachment_id = fields.Many2many('ir.attachment', string="Attachment")
    tag_id = fields.Many2one('attachment.tag', "Category")


class SaleAttachments(models.Model):
    _name = 'sale.attachments'

    sale_id = fields.Many2one('sale.order')
    attachment_id = fields.Many2many('ir.attachment', string="Attachment")
    tag_id = fields.Many2one('attachment.tag', "Category")


class AttachmentTag(models.Model):
    _name = 'attachment.tag'

    name = fields.Char("Category")
