# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) PySquad Informetics (<https://www.pysquad.com/>).
#
#    For Module Support : contact@pysquad.com
#
##############################################################################

{
    'name': 'statement amount',
    'version': '15.0',
    'category': 'account',
    'summary': 'Odoo module for customizable merging of purchase orders',
    'description': """
            This module allows users to merge purchase orders with different merge types, providing flexibility
            in handling purchase orders based on specific requirements and workflows.
            """,

    'author': 'Pysquad Informatics LLP',
    'website': 'https://www.pysquad.com',
    'depends': ['base', 'account'],
    'data': [
        # "security/ir.model.access.csv",
        # "views/inherit_purchse_order_view.xml",
        "views/custom_amount.xml",
        # "wizard/ps_merge_purchase_order_view.xml",
    ],
    # 'images': [
    #     'static/description/merge_po_banner.jpg',
    # ],
}