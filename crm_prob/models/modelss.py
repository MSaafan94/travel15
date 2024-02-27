# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmProbability(models.Model):
    _inherit = 'crm.lead'

    custom_probability = fields.Integer(compute='custom_probability_method', store=True)

    passport_check = fields.Boolean()
    professional_job_check = fields.Boolean()
    bank_account_check = fields.Boolean()
    visas_check = fields.Boolean()
    bachelor_check = fields.Boolean()

    @api.depends('passport_check', 'professional_job_check', 'bank_account_check', 'visas_check', 'bachelor_check')
    def custom_probability_method(self):
        for record in self:
            custom_probability = 0
            if record.passport_check:
                custom_probability += 10
            if record.professional_job_check:
                custom_probability += 20
            if record.bank_account_check:
                custom_probability += 30
            if record.visas_check:
                custom_probability += 30
            if record.bachelor_check:
                custom_probability += 10
            record.custom_probability = custom_probability
