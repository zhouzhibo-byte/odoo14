# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class PemWages(models.Model):
    _name = 'pem.wages'
    _description = "工资条目"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('工资表编号', required=True, readonly=True, index=True, copy=False, default='新建')
    user_name=fields.Many2one('res.users','创建人',default=lambda self: self.env.user, track_visibility='onchange')
    date = fields.Date('创建时间', readonly=True, copy=False, default=fields.Date.today)
    company_id = fields.Many2one('res.company', '公司', readonly=True, default=lambda self: self.env.user.company_id)
    wages_line_ids = fields.One2many('pem.wages.line', 'pem_wages_id', '个人所得税明细', redonly=True,
                                   copy=True)
    state = fields.Selection([('draft', '草稿'),
                              ('approve', '审批'),
                              ('complete', '完成')], '状态', default='draft', track_visibility='always')

    @api.model
    def create(self, vals):
        if vals.get('name', '新建') == '新建':
            vals['name'] = self.env['ir.sequence'].next_by_code('pem.wages') or '/'
        result = super(PemWages, self).create(vals)
        return result

    #
    def action_approve(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('只有在草稿状态下才可以提交')
        self.write({'state': 'approve'})
        return True

    #
    def action_complete(self):
        self.ensure_one()
        if self.state != 'approve':
            raise UserError('只有在审批状态下才可以提交')
        self.write({'state': 'complete'})
        return True

    #
    def action_create(self):
        self.ensure_one()
        if self.state != 'complete':
            raise UserError('只有在完成状态下才可以提交')
        self.create_pem_personal_tax()
        self.create_pem_social_insurance()
        self.create_pem_accumulation_fund()

        view_name = 'pem_wages_view_finish_form'
        module = 'personnel_expense_management'
        view = self.env['ir.model.data'].search([('name', '=', view_name), ('module', '=', module)])
        view_id = view.res_id
        return {
            'name': '工资',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'flags': {'initial_mode': 'view', 'action_buttons': False},
            'res_model': 'pem.wages',
        }

    def create_pem_personal_tax(self):
        self.ensure_one()
        pem_personal_tax_id = self.env['pem.personal.tax'].sudo().search([('user_name', '=', self.user_name.id)])
        if len(pem_personal_tax_id) != 0:
            raise UserError(("当前创建人%s已存在个人所得税记录！") % self.user_name.login)
        else:
            pem_personal_tax_vals = {
                'user_name': self.user_name.id,
                'date': self.date,
                'company_id': self.company_id.id
            }
            pem_personal_tax_id = self.env['pem.personal.tax'].sudo().create(pem_personal_tax_vals)
            for line in self.wages_line_ids:
                pem_personal_tax_line_vals = {
                    'user_id': line.user_id.id,
                    'provided_company_id': line.provided_company_id.id,
                    'pem_personal_tax_id': pem_personal_tax_id.id
                }
            self.env['pem.personal.tax.line'].sudo().create(pem_personal_tax_line_vals)
        return True

    def create_pem_social_insurance(self):
        self.ensure_one()
        pem_social_insurance_id = self.env['pem.social.insurance'].sudo().search([('user_name', '=', self.user_name.id)])
        if len(pem_social_insurance_id) != 0:
            raise UserError(("当前创建人%s已存在社保记录！") % self.user_name.login)
        else:
            pem_social_insurance_vals = {
                'user_name': self.user_name.id,
                'date': self.date,
                'company_id': self.company_id.id
            }
            pem_social_insurance_id = self.env['pem.social.insurance'].sudo().create(pem_social_insurance_vals)
            for line in self.wages_line_ids:
                pem_social_insurance_line_vals = {
                    'user_id': line.user_id.id,
                    'provided_company_id': line.provided_company_id.id,
                    'pem_social_insurance_id': pem_social_insurance_id.id
                }
            self.env['pem.social.insurance.line'].sudo().create(pem_social_insurance_line_vals)
        return True

    def create_pem_accumulation_fund(self):
        self.ensure_one()
        pem_accumulation_fund_id = self.env['pem.accumulation.fund'].sudo().search([('user_name', '=', self.user_name.id)])
        if len(pem_accumulation_fund_id) != 0:
            raise UserError(("当前创建人%s已存在公积金记录！") % self.user_name.login)
        else:
            pem_accumulation_fund_vals = {
                'user_name': self.user_name.id,
                'date': self.date,
                'company_id': self.company_id.id
            }
            pem_accumulation_fund_id = self.env['pem.accumulation.fund'].sudo().create(pem_accumulation_fund_vals)
            for line in self.wages_line_ids:
                pem_accumulation_fund_line_vals={
                    'user_id':line.user_id.id,
                    'provided_company_id':line.provided_company_id.id,
                    'pem_accumulation_fund_id':pem_accumulation_fund_id.id
                }
            self.env['pem.accumulation.fund.line'].sudo().create(pem_accumulation_fund_line_vals)
        return True

class PemWagesLine(models.Model):
    _name = 'pem.wages.line'
    _description = "工资明细表"

    user_id = fields.Many2one('res.users', '姓名', default=lambda self: self.env.user, track_visibility='onchange')
    account_payable=fields.Float('应发',track_visibility='onchange', digits=(10, 3))
    account_payment = fields.Float('实发',track_visibility='onchange',digits=(10, 3))
    resource_travel_expenses = fields.Float('人资差旅费',track_visibility='onchange',digits=(10, 3))
    provided_company_id=fields.Many2one('res.company', '发放公司')
    pem_wages_id = fields.Many2one('pem.wages', '工资表')

    #
    def action_pem_salary_related_expenses_details(self):
        view_name ='pa_pay_slip_part_view_form'
        module='personnel_expense_management'
        view = self.env['ir.model.data'].search([('name', '=', view_name),('module','=',module)])
        view_id = view.res_id
        return {
            'name': '工资相关费用明细',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
             'flags':{'initial_mode': 'view', 'action_buttons': False},
            'res_model': 'pa.pay.slip',
            'domain':[('name','=',self.user_id)]
        }
