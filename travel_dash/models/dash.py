from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EmployeeData(models.Model):
    _name = 'my_employee_module.employee_data'
    _description = 'Employee Data'

    name = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        help="Link to the employee in the HR module."
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        related='name.department_id',
        readonly=True,
        store=True,
        help="Department of the employee."
    )
    salary = fields.Float(string='Salary')
    deduction = fields.Float(string='Deduction')
    commission = fields.Float(string='Commission')
    revenue = fields.Float(string='Revenue')
    cost = fields.Float(string='Cost')
    month = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
         ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
         ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month',
        required=True
    )

    profit = fields.Float(string='Profit', readonly=True)
    net_profit = fields.Float(string='Net Profit', readonly=True)
    total_cost_per_lead = fields.Float(string='Total Cost per Lead', readonly=True)

    _is_calculating_values = fields.Boolean(string='Is Calculating Values', default=False, store=False)

    @api.model
    def create(self, values):
        record = super(EmployeeData, self).create(values)
        record._calculate_values()
        return record

    def write(self, values):
        res = super(EmployeeData, self).write(values)

        # Check if the relevant fields have changed before triggering the calculation
        if any(field in values for field in ['month', 'revenue', 'cost', 'commission', 'salary', 'deduction']):
            for record in self:
                record._calculate_values()

        return res

    def _calculate_values(self):
        for record in self:
            if not record._is_calculating_values:
                record._is_calculating_values = True

                record.profit = record.revenue - record.cost
                record.net_profit = record.revenue - record.cost - record.commission - record.salary + record.deduction - record.total_cost_per_lead

                # Calculate total sales order for the specified salesperson and month
                today = datetime.today()
                current_year = today.year
                current_month = today.month

                selected_month = int(record.month)
                if current_month < selected_month:
                    current_year -= 1

                start_date = datetime(current_year, selected_month, 1)
                end_date = (start_date + relativedelta(months=1, days=-1)).replace(hour=23, minute=59, second=59)

                costperlead = record.env['crm.lead'].search([
                    ('user_id', '=', record.name.user_id.id),  # Assuming user_id represents the salesperson
                    ('create_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
                    ('create_date', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S')),
                ])
                print(costperlead)

                # Calculate total cost_per_lead
                record.total_cost_per_lead = sum(costperlead.mapped('x_studio_cost_per_lead'))
                print(record.total_cost_per_lead)

                # Calculate revenue
                total_sales_order = record.env['sale.order'].search([
                    ('user_id', '=', record.name.user_id.id),  # Assuming user_id represents the salesperson
                    ('date_order', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
                    ('date_order', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S')),
                    ('state', 'in', ['sale', 'done']),  # Include confirmed and completed sales orders
                ]).mapped('amount_total')

                record.revenue = sum(total_sales_order)

                record._is_calculating_values = False
