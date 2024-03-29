from odoo import fields, models, api
from datetime import date, datetime,timedelta
import datetime
from odoo.exceptions import ValidationError, UserError

import logging


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char(required=True)
    phone = fields.Char(required=True)
    service_type = fields.Many2one('service.type', "Service Type", required=True)
    whatsapp_num = fields.Char("WhatsApp Number")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default="male")
    birthday = fields.Date("Birthday")
    years = fields.Integer("Years", compute='_check_employee_age', store=True)
    months = fields.Integer("Months", compute='_check_employee_age', store=True)
    days = fields.Integer("Days", compute='_check_employee_age', store=True)
    age_type = fields.Selection([('infant', 'Infant'),
                                 ('child', 'Child'),
                                 ('adult', 'Adult')], string="Age Type", compute='_check_employee_age', store=True)
    email = fields.Char("Email")
    trip_code = fields.Char("Trip Code")
    passport_num = fields.Char("Passport Number")
    passport_expiry = fields.Date("Passport Expiry Date")
    lead_source = fields.Many2one("utm.source",)
    id_number = fields.Char("ID Number")
    destination_1 = fields.Many2one('destination', "Destination 1")
    booking_status = fields.Many2one('booking.status', "Booking Status")
    Description = fields.Text("Description")
    owner = fields.Char("Owner")
    # created_at = fields.Datetime("Created at", )


    won_date = fields.Date(string="Won Date", readonly=True, store=True, compute='_compute_won_date')

    @api.depends('stage_id')
    def _compute_won_date(self):
        for lead in self:
            if lead.stage_id and lead.stage_id.is_won:
                lead.won_date = fields.Date.today()
            else:
                lead.won_date = False

    def open_whatsapp_web(self):
        if len(self.whatsapp_num) <= 11:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://wa.me/+2{}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://wa.me/{}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))

    def open_whatsapp_mobile(self):
        if len(self.whatsapp_num) <= 11:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone=+2{}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone={}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))

    # def calculate_stage_time(self):
    #     # domain=[]
    #     hh = self.env['crm.lead'].search([('stage_id', '=', 'new')])
    #     print(hh)
    #     print('asdfasdfhgjasdfuyaswdgfwjhefgasjkdhfgkasjdhfgjasdhfa')

    def get_new_leads_more_than_a_dayy(self):
        # try:
        leads = self.env['crm.lead'].search([('stage_id', '=', 1), ])
        print(len(leads))
        lead_count = self.env['crm.lead'].search_count([('stage_id', '=', 1), ('active', '=', True),
                                                        ('create_date', '<', date.today())])
        print(lead_count)
        # for sale_order in leads:
        #     print(sale_order)
        # except:
        #     return "internal error"

    # @api.model
    # def get_new_leads_more_than_a_day(self):
    #     """Method to get leads that have been in the new stage for more than a day."""
    #     one_day_ago = datetime.now() - timedelta(days=1)
    #     # new_stage = self.env.ref('crm.new')  # replace with the ID or name of your new stage
    #     leads = self.search([('stage_id', '=', 'new'),])
    #     print(len(leads))
    #     return leads

    @api.onchange('partner_id')
    def _fill_contact_data(self):
        self.service_type = self.partner_id.service_type
        self.whatsapp_num = self.partner_id.whatsapp_num
        self.gender = self.partner_id.gender
        self.birthday = self.partner_id.birthday
        self.years = self.partner_id.years
        self.months = self.partner_id.months
        self.days = self.partner_id.days
        self.trip_code = self.partner_id.trip_code
        self.passport_num = self.partner_id.passport_num
        self.passport_expiry = self.partner_id.passport_expiry
        self.lead_source = self.partner_id.lead_source
        self.id_number = self.partner_id.id_number
        self.destination_1 = self.partner_id.destination_1
        self.booking_status = self.partner_id.booking_status
        self.owner = self.partner_id.owner
        # self.created_at = self.partner_id.created_at
        self.Description = self.partner_id.Description

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        change = self._change_contact_data(vals)
        return res

    # @api.onchange('service_type','whatsapp_num','gender','birthday','years','months','days','trip_code','passport_expiry','passport_num','lead_source','id_number','destination_1','booking_status','owner','created_at','Description')
    def _change_contact_data(self, vals):
        if vals.get('partner_id'):
            partner = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
            partner['service_type'] = vals.get('service_type')
            partner['whatsapp_num'] = vals.get('whatsapp_num')
            partner['gender'] = vals.get('gender')
            partner['birthday'] = vals.get('birthday')
            partner['years'] = vals.get('years')
            partner['months'] = vals.get('months')
            partner['days'] = vals.get('days')
            partner['trip_code'] = vals.get('trip_code')
            partner['passport_num'] = vals.get('passport_num')
            partner['passport_expiry'] = vals.get('passport_expiry')
            partner['lead_source'] = vals.get('lead_source')
            partner['id_number'] = vals.get('id_number')
            partner['destination_1'] = vals.get('destination_1')
            partner['booking_status'] = vals.get('booking_status')
            partner['owner'] = vals.get('owner')
            # partner['created_at'] = vals.get('created_at')
            partner['Description'] = vals.get('Description')

    @api.depends('birthday')
    def _check_employee_age(self):
        for rec in self:
            if rec.birthday:
                today = datetime.date.today()
                birthdate = rec.birthday
                age_in_days = (today - birthdate).days
                years = age_in_days // 365
                remaining_days = age_in_days % 365
                months = remaining_days // 30
                days = remaining_days % 30
                rec.years = years
                rec.months = months
                rec.days = days
                if years < 2:
                    rec.age_type = 'infant'
                elif years < 12:
                    rec.age_type = 'child'
                else:
                    rec.age_type = 'adult'

    def get_transfer_wizard(self):
        ctx = self.env.context
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Sales Person',
            'res_model': 'transfer.salesperson',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sales_extra_fields.transfer_salesperson_view_form').id,
            'target': 'new',
            'context': ctx
        }


class ServiceType(models.Model):
    _name = 'service.type'

    name = fields.Char("Service Type")


class Destination(models.Model):
    _name = 'destination'

    name = fields.Char("Destination")


class BookingStatus(models.Model):
    _name = 'booking.status'

    name = fields.Char("Destination")
