# -*- coding: utf-8 -*-
{
    'name': "travelsawa_details",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'crm', 'hr', 'sales_team', 'stock', 'sales_extra_fields', 'account', 'stock_account', 'purchase', 'contacts', 'travel_sales', 'mail', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/xlxs_reports.xml',
        'views/templates.xml',
        'views/details.xml',
        'views/quot_temp.xml',
        'views/purchase.xml',
        # 'views/invoice.xml',
        'security/security.xml',
        'security/sec.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}