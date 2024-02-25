from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PartnerRelationship(models.Model):
    _name = 'partner.relationshipp'
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


class SaleVieww(models.Model):
    _inherit = 'sale.order'

    relationship_ids = fields.One2many('partner.relationshipp', 'relation_id', string='Relationships')

    def name_get(self):
        result = []
        for record in self:
            name = record.partner_id.name if record.partner_id else ''
            result.append((record.id, name))
        return result

    # @api.model
    # def create(self, vals):
    #     templates = super(SaleView, self).write(vals)
    #
    #     # fix attachment ownership
    #     for rec in self.relationship_ids:
    #         if rec.attachment_ids:
    #             rec.attachment_ids.write({'res_model': self._name, 'res_id': rec.id})
    #     return templates


class CrmLeadd(models.Model):
    _inherit = 'crm.lead'

    # def action_sale_quotations_new(self):
    #     res = super(CrmLeadd, self).action_sale_quotations_new()
    #     if not self.partner_id:
    #         print('sadfsdfasdfadsfasdfasdf')
    #         raise ValidationError("Cannot create quotation: Lead does not have a customer.")
    #     else:
    #         print('ooooooooooooooo')
    #         return res

    # def action_new_quotation(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
    #     action['context'] = {
    #         'search_default_opportunity_id': self.id,
    #         'default_opportunity_id': self.id,
    #         'search_default_partner_id': self.partner_id.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_campaign_id': self.campaign_id.id,
    #         'default_medium_id': self.medium_id.id,
    #         'default_origin': self.name,
    #         'default_source_id': self.source_id.id,
    #         'default_company_id': self.company_id.id or self.env.company.id,
    #         'default_tag_ids': [(6, 0, self.tag_ids.ids)]
    #     }
    #     if self.team_id:
    #         action['context']['default_team_id'] = self.team_id.id,
    #     if self.user_id:
    #         action['context']['default_user_id'] = self.user_id.id
    #     return action



    # def create_sale_quotation(self):
    #     # Check if the lead has a customer
    #     if not self.partner_id:
    #         raise ValidationError("Cannot create quotation: Lead does not have a customer.")
    #
    #     # Create quotation logic here
    #     # Example: You can create a sale order or open the quotation form view
    #     # For example, to create a sale order:
    #     sale_order = self.env['sale.order'].create({
    #         'partner_id': self.partner_id.id,
    #         # Add other necessary fields
    #     })
    #     # Navigate to the sale order view
    #     return {
    #         'name': 'Sale Order',
    #         'view_mode': 'form',
    #         'res_model': 'sale.order',
    #         'res_id': sale_order.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #     }

    relationship_ids = fields.One2many('partner.relationshipp', 'relation_id', string='Relationships')
    acquisition_lead = fields.Many2one('utm.source')
    education = fields.Many2one('education')
    region = fields.Many2one('region')
    area = fields.Many2one('area')
    profession = fields.Many2one('profession')

    # reason = fields.Many2one('disqualified')

    def create_customer_from_crm(self):
        existing_contact = self.env['res.partner'].search([('phone', '=', self.phone)], limit=1)

        if existing_contact:
            # If an existing contact is found, update its fields
            self.acquisition_lead = existing_contact.acquisition_lead
            existing_contact.write({
                # 'name': self.name,
                'whatsapp_num': self.whatsapp_num,
                'birthday': self.birthday,
                'passport_num': self.passport_num,
                'passport_expiry': self.passport_expiry,
                'id_number': self.id_number,
                'email': self.email_from,

                # 'service_type': self.service_type.id if self.service_type else False,
                # Update other fields as needed
            })
            self.partner_id = existing_contact.id
        else:

            self.acquisition_lead = self.source_id
            # If no existing contact is found, create a new customer
            new_customer = self.env['res.partner'].create({
                'name': self.name,
                'phone': self.phone,
                'whatsapp_num': self.whatsapp_num,
                'birthday': self.birthday,
                'passport_num': self.passport_num,
                'passport_expiry': self.passport_expiry,
                'id_number': self.id_number,
                'email': self.email_from,
                'acquisition_lead': self.acquisition_lead
                # 'service_type': self.service_type.id if self.service_type else False,
                # You can fill other fields here based on CRM data
            })
            self.partner_id = new_customer.id

    def _find_matching_partner_by_phone(self):
        """
        Find a matching partner by phone number.
        """
        # Assuming phone number is stored in the field 'phone'
        matching_partner = self.env['res.partner'].search([('phone', '=', self.phone)], limit=1)
        if matching_partner:
            self.acquisition_lead = matching_partner.acquisition_lead
        return matching_partner

    @api.model
    def create_opportunity(self, lead_id, customer_phone):
        # Search for existing customer with matching phone number
        existing_customer = self.env['res.partner'].search([('phone', '=', customer_phone)], limit=1)

        # If a matching customer is found, link the lead to the customer
        if existing_customer:
            lead = self.browse(lead_id)
            lead.partner_id = existing_customer.id
            # You might want to update other lead fields here

        # Proceed with regular lead conversion process
        return super(CrmLeadd, self).create_opportunity(lead_id)


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


class CustomCrmLead(models.Model):
    _inherit = 'crm.lead'

    stage_name = fields.Char(related='stage_id.name', string='Stage')

    status_changed = fields.Boolean(string="Status Changed", default=False)
    first_action_date = fields.Date(string="First Action Date")

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self._origin.stage_id != self.stage_id:
            if not self.status_changed:
                self.first_action_date = fields.Date.today()
                self.status_changed = True

    # @api.model
    # def create(self, vals):
    #     new_lead = super(CustomCrmLead, self).create(vals)
    #
    #     # Call autofill_leads_customer method for the newly created lead
    #     new_lead.autofill_leads_customer()
    #
    #     return new_lead

    def autofill_leads_customer(self):
        # Initialize counter for total leads processed
        total_leads_processed = 0

        # Define batch size
        batch_size = 1000

        # Define starting offset
        offset = 0

        # Fetch leads in batches until all leads are processed
        while True:
            # Fetch leads in batches
            leads = self.search([('partner_id', '=', False)], limit=batch_size, offset=offset)

            # Break the loop if no more leads are found
            if not leads:
                break

            # Increment offset for the next batch
            offset += batch_size

            # Fetch contacts with a non-empty phone field
            contacts = self.env['res.partner'].search([('phone', '!=', False)])

            # Process leads in the current batch
            for lead in leads:
                # Filter contacts based on lead phone numbers
                matching_contacts = contacts.filtered(lambda c: c.phone == lead.phone)
                if matching_contacts:
                    # Choose the first matching contact and assign it to the lead
                    lead.partner_id = matching_contacts[0].id
                    total_leads_processed += 1  # Increment counter

        print(f"Total leads processed: {total_leads_processed}")

    # def write(self, vals):
    #     # Call super to perform the write operation
    #     res = super(CustomCrmLead, self).write(vals)
    #
    #     # Call autofill_leads_customer method for the newly created lead
    #     self.autofill_leads_customer()
    #
    #     return res

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


class ContactUpdate(models.Model):
    _inherit = 'res.partner'
    acquisition_lead = fields.Many2one('utm.source')


class SaleOrderr(models.Model):
    _inherit = 'sale.order'

    # is_duplicated = fields.Selection([('update', 'update'), ('confirmed', 'confirmed')])

    def action_cancel(self):
        # Call super to perform the cancellation of the sale order
        res = super(SaleOrderr, self).action_cancel()

        # Update opportunity stage to 'cancel' for related opportunities
        canceled_stage = self.env['crm.stage'].search([('name', '=', 'Canceled')], limit=1)
        for order in self:
            if order.opportunity_id:
                order.opportunity_id.stage_id = canceled_stage.id
        return res

    def action_confirm(self):
        res = super(SaleOrderr, self).action_confirm()

        won_stage = self.env['crm.stage'].search([('name', '=', 'won')], limit=1)

        for order in self:
            if order.opportunity_id:
                order.opportunity_id.stage_id = won_stage.id
        return res
