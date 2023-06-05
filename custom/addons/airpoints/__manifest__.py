# -*- coding: utf-8 -*-
{
    'name': "Airpoints",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Saafan",
    'website': "http://www.Saafan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'App',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'crm', 'account', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_to_invoice.xml',
        'wizard/transfer_salesperson.xml',
    ],
    # only loaded in demonstration mode
}