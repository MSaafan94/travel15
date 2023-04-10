# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2022 Zone4Erp SSolutions (<zone4erp@gmail.com>).
#
#    For Module Support : zone4erp@gmail.com
#
##############################################################################

{
    'name': 'Sale Advance Payment Register',
    'version': '15.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Sales',
    'description':
        """        
        This Module will helps to register a payment in advance on the Quotation / Sales Order itself.
    """,
    'summary': 'This Module will helps to register a payment in advance on the Quotation / Sales Order itself',
    'depends': ['base','sale_management','account'],
    'images': ['static/description/SAP_15.png'],
    'data': ['security/ir.model.access.csv',
             'views/sale_order_view.xml',],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'author': 'Zone4Erp Solutions',
    'website': 'zone4erp@gmail.com',
    'maintainer': 'Zone4Erp Solutions',
    'support': 'zone4erp@gmail.com',
    'price': 9.5,
    'currency': 'USD',

}
