import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from psycopg2 import sql

from odoo import api, fields, models, tools, SUPERUSER_ID


class CustomCrmLead(models.Model):
    _inherit = 'crm.lead'

    stage_name = fields.Char(related='stage_id.name', string='Stage')

    # @api.model
    # def create(self, vals):
    #     new_lead = super(CustomCrmLead, self).create(vals)
    #
    #     # Call autofill_leads_customer method for the newly created lead
    #     new_lead.autofill_leads_customer()
    #
    #     return new_lead

    def autofill_leads_customer(self):
        # Fetch leads in batches of 1000 records
        leads = self.search([('partner_id', '=', False)], limit=1000)

        contacts = self.env['res.partner'].search([])  # Fetch all contacts

        for lead in leads:
            # Filter contacts based on lead phone numbers
            matching_contacts = contacts.filtered(lambda c: c.phone == lead.phone)
            if matching_contacts:
                # Choose the first matching contact and assign it to the lead
                lead.partner_id = matching_contacts[0].id

    @api.depends('phone')
    def _compute_potential_lead_duplicates(self):
        MIN_PHONE_LENGTH = 11  # Assuming a minimum length for a valid phone number
        SEARCH_RESULT_LIMIT = 21

        def return_if_relevant(model_name, domain):
            """ Returns the recordset obtained by performing a search on the provided
            model with the provided domain if the cardinality of that recordset is
            below a given threshold (i.e: `SEARCH_RESULT_LIMIT`). Otherwise, returns
            an empty recordset of the provided model as it indicates search term
            was not relevant.

            Note: The function will use the administrator privileges to guarantee
            that a maximum amount of leads will be included in the search results
            and transcend multi-company record rules. It also includes archived records.
            Idea is that counter indicates duplicates are present and that lead
            could be escalated to managers.
            """
            # Includes archived records and transcends multi-company record rules
            model = self.env[model_name].sudo().with_context(active_test=False)
            res = model.search(domain, limit=SEARCH_RESULT_LIMIT)
            return res if len(res) < SEARCH_RESULT_LIMIT else self.env[model_name]

        for lead in self:
            lead_id = lead._origin.id if isinstance(lead.id, models.NewId) else lead.id
            common_lead_domain = [
                ('id', '!=', lead_id)
            ]

            duplicate_lead_ids = self.env['crm.lead']
            phone_search = lead.phone

            if phone_search and len(phone_search) >= MIN_PHONE_LENGTH:
                duplicate_lead_ids |= return_if_relevant('crm.lead', common_lead_domain + [
                    ('phone', '=', phone_search)
                ])

            lead.duplicate_lead_ids = duplicate_lead_ids + lead
            lead.duplicate_lead_count = len(duplicate_lead_ids)
