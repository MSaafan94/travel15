# -*- coding: utf-8 -*-
{
    'name': "Masked Telephone Widget",
    'version': '15.0.1.0.0',
    'author': "kerd29, fatatoo",
    'category': 'Extra Tools',
    'website': "fatuca2019@gmail.com",
    'summary': "International Telephone Masked Input Widget",
    'depends': ['web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'phone_country_widget/static/lib/intl-tel-input/css/intlTelInput.css',
            'phone_country_widget/static/src/scss/phone_widget.scss',
            'phone_country_widget/static/lib/intl-tel-input/js/utils.js',
            'phone_country_widget/static/lib/intl-tel-input/js/intlTelInput-jquery.js',
            'phone_country_widget/static/lib/jQuery-Mask/jquery.mask.js',
            'phone_country_widget/static/src/js/phone_widget.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
