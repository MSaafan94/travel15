from odoo import models, fields , api


class EmployeeData(models.Model):
    _name = 'my_dep_module.dep_data'
    _description = 'Employee Department'

    name = fields.Many2one(
        'hr.department',
        string='Employee',
        required=True,
        help="Link to the employee in the HR module."
    )

    salary = fields.Float(string='Salary')
    commission = fields.Float(string='Commission')
    revenue = fields.Float(string='Revenue')
    cost = fields.Float(string='Cost')
    profit = fields.Float(string='Profit', compute='_compute_profit', store=True)
    month = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
         ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
         ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month',
        required=True
    )

    # monthly_progress_ids = fields.One2many(
    #     'my_employee_module.monthly_progress',
    #     'employee_id',
    #     string='Monthly Progress'
    # )

    @api.depends('revenue', 'cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.revenue - record.cost
