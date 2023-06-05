# -*- coding: utf-8 -*-
{
    'name': "Global Solutions JournaL Entry Report",

    'summary': "Global Solutions JournaL Entry Report",

    'description': "Global Solutions JournaL Entry Report",

    'author': "Saafa  Solutions",
    'website': "https://Saafan.dev",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sale', 'sale_management', 'crm', 'account', 'hr'],
    'license': 'OPL-1',
    # always loaded
    'data': [
        'wizard/wizard_view.xml',
        'views/menu.xml',
        'views/sales_to_invoice.xml',
        'reports/report.xml',
        'security/ir.model.access.csv',
    ],
}
