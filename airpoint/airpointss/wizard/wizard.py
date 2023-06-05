from odoo import api, fields, models


class JournalItemsReportWizard(models.TransientModel):
    _name = "journal.items.wizard"
    _description = "Journal Items Report Wizard"

    partner_id = fields.Many2one("res.partner", string="Partner")
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")

    def print_report(self):
        domain = []
        if self.partner_id:
            domain.append(("partner_id", "=", self.partner_id.id))
        if self.date_from:
            domain.append(("date", ">=", self.date_from))
        if self.date_to:
            domain.append(("date", "<=", self.date_to))

        data = {
            "domain": domain,
            "order": "date",
        }

        context = {
            "partner_name": self.partner_id.name,
            "from_date": self.date_from,
            "to_date": self.date_to,
        }

        return self.env.ref("airpointss.journal_items_report_action").with_context(**context).report_action(self,
                                                                                                            data=data)