from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TransferSalesPerson(models.TransientModel):
    _name = 'transfer.salesperson'
    _description = 'Transfer salesPerson'

    employee_id = fields.Many2one('hr.employee', "Employee", required=1)

    def transfer_sales_person(self):
        model = self.env.context.get('active_model')
        crm_ids = self.env[model].browse(self.env.context.get('active_ids'))
        for lead in crm_ids:
            if not self.employee_id.user_id:
                raise UserError(_("You Should Set User for Employee %s") % (self.employee_id.name))
            else:
                lead.user_id = self.employee_id.user_id.id

# class TransferSalesPerson(models.TransientModel):
#     _name = 'transfer.salesperson'
#     _description = 'Transfer SalesPerson Wizard'
#
#     employee_id = fields.Many2one('res.users', "New Salesperson", required=True)
#
#     def transfer_sales_person(self):
#         active_ids = self.env.context.get('active_ids', [])
#         if active_ids:
#             leads = self.env['crm.lead'].browse(active_ids)
#             leads.write({'user_id': self.employee_id.id})
#         return {'type': 'ir.actions.act_window_close'}

