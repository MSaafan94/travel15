# -*- coding: utf-8 -*-
{
    'name': "travel_dash",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Saafan",
    'website': "http://www.saafan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'App',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'hr', 'crm'],

    # always loaded
    'data': [
        'views/dash.xml',
        'views/dep_dash.xml',
        'views/custom_crm_cost_per_lead.xml',
        'views/lead_cost_views.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode

}