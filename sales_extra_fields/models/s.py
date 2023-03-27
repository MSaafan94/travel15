from odoo import api, models


from odoo import api, models

class CrmLeads(models.Model):
    _inherit = 'crm.lead'

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     # Get the current user's team
    #     user = self.env.user
    #     team = user.sale_team_id
    #
    #     # Add a domain filter to limit results to leads assigned to the user's team
    #     args.append(('team_id', '=', team.id))
    #
    #     return super(CrmLeads, self).search(args, offset=offset, limit=limit, order=order, count=count)


