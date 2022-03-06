# -*- coding: utf-8 -*-
{
    'name': "personnel_expense_management",
    'summary': """
        人员给用管理""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Ruisi",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        # 'groups/permission_group.xml',
    # 'groups/rule_security.xml',
        'security/ir.model.access.csv',

        'views/pem_personal_tax.xml',
        'views/pem_social insurance.xml',
        'views/pem_accumulation_fund.xml',
        'views/pem_wages.xml',
        'views/pa_pay_slip_part_view.xml',
        'views/menuitems.xml',
    ],
    'application': True,
    'installable': True,
}