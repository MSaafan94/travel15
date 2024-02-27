from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.depends('lead_id')
    def _compute_action(self):
        for convert in self:
            if not convert.lead_id:
                convert.action = 'nothing'
            else:
                matching_partner = convert.lead_id._find_matching_partner_by_phone()
                if matching_partner:
                    convert.action = 'exist'
                    convert.partner_id = matching_partner.id
                elif convert.lead_id.contact_name:
                    convert.action = 'create'
                else:
                    convert.action = 'nothing'


class PartnerRelationship(models.Model):
    _name = 'partner.relationship'
    relation_id = fields.Integer()
    name = fields.Char(string='Name')
    relationship = fields.Selection([('father', 'Father'),
                                     ('mother', 'Mother'),
                                     ('son', 'Son'),
                                     ('daughter', 'Daughter'),
                                     ('husband', 'Husband'),
                                     ('wife', 'Wife'),
                                     ('brother', 'Brother'),
                                     ('sister', 'Sister'),
                                     ('grandfather', 'Grandfather'),
                                     ('grandmother', 'Grandmother'),
                                     ('uncle', 'Uncle'),
                                     ('aunt', 'Aunt'),
                                     ('cousin', 'Cousin'),
                                     ('fiance', 'Fiance'),
                                     ('friend', 'Friend')], string="Relationship")
    number = fields.Char(string='Number')
    expiry_date = fields.Date()
    attachment_ids = fields.Many2one('ir.attachment', string='Attachments')
    # attachment_idss = fields.One2many('sale.attachments', 'sale_id', "Attachments", track_visibility='always')



class Education(models.Model):
    _name = 'edu.education'
    name = fields.Char()


class Region(models.Model):
    _name = 'reg.region'
    name = fields.Char()


class Area(models.Model):
    _name = 'are.area'
    name = fields.Char()


class Profession(models.Model):
    _name = 'pro.profession'
    name = fields.Char()

