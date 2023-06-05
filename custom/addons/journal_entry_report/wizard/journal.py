from odoo import models, fields, api
from odoo.exceptions import UserError


class CRMLead(models.Model):
    _inherit = "account.move.line"

    def journal_report_wizard(self):
        ctx = self.env.context
        return {
            'type': 'ir.actions.act_window',
            'name': 'Set fields',
            'res_model': 'journal.report',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('journal_entry_report.journal_report', False).id,
            'target': 'new',
            'context': ctx
        }


class JournalReportWizard(models.TransientModel):
    _name = 'journal.report'
    _description = 'Journal Report'

    # employee_id = fields.Many2one('hr.employee', "Employee", required=1)
    partner = fields.Many2one('res.partner')
    from_date = fields.Date()
    to_date = fields.Date()

    def transfer_sales_person(self):
        model = self.env.context.get('active_model')
        journal_ids = self.env[model].browse(self.env.context.get('active_ids'))

