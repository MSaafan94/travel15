from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TransferSalesPerson(models.TransientModel):
    """This model is used to transfer a salesperson from one lead to another."""

    _name = 'transfer.salesperson'
    _description = 'Transfer SalesPerson'

    employee_id = fields.Many2one('res.users', "User", required=True)

    def transfer_sales_person(self):
        """
        This method transfers the salesperson associated with the active model's leads
        to the salesperson associated with the selected user.
        """
        active_model_name = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')

        # Get all leads associated with the active model
        leads = self.env[active_model_name].browse(active_ids)

        # Transfer the salesperson for each lead
        for lead in leads:
            if not self.employee_id:
                # Raise an error if the user doesn't exist
                raise UserError(f"The user {self.employee_id.name} does not exist.")
            else:
                # Transfer the salesperson
                lead.user_id = self.employee_id.id
