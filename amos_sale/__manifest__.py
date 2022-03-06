# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'Amous销售订单',
    'version': '1.1',
    'summary': u'报价单和销售订单',
    'sequence': 10,
    'description': """
    销售模块
     """,
    'category': u'amouserp',
    'website': 'https://www.odoo.com/page/billing/sda',
    # 'images' : ['images/accounts.jpeg'],
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/wl_plan.xml',
        'views/wl_product_type.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_account_post_init',
}
