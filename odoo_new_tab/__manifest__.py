# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "View Records In New Tab",
  "summary"              :  """Odoo view records in new tab facilitates Odoo User to open a form for any record in new tab with a click.""",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-View-Records-In-New-Tab.html",
  "description"          :  """View Records In New Tab
Odoo View Records in new tab
View Records
New Tab to View Records
New Tab in Odoo to View Records
Open Records in new Tab
Opening the Records in New Tab
See Records in new tab""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_new_tab",
  "depends"              :  ['web'],
  "data"                 :  ['views/template.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  10,
  "currency"             :  "USD",
  "assets": {
        'web.assets_backend': [
            'odoo_new_tab/static/src/js/list_view.js',
        ],
    },
  "pre_init_hook"        :  "pre_init_check",
}