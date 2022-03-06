# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class PemSocialInsurance(models.Model):
    _name = 'pem.social.insurance'
    _description = "社保"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('社保表编号', required=True, readonly=True, index=True, copy=False, default='新建')
    user_name = fields.Many2one('res.users', '创建人', default=lambda self: self.env.user, track_visibility='onchange')
    date = fields.Date('创建时间', readonly=True, copy=False, default=fields.Date.today)
    total_company_social_insurance=fields.Float('公司应付社保合计',compute='compute_total_social_insurance', store=True,track_visibility='always', digits=(10, 3))
    total_personal_social_insurance=fields.Float('个人应付社保合计',compute='compute_total_social_insurance', store=True,track_visibility='always', digits=(10, 3))
    company_id = fields.Many2one('res.company', '公司', readonly=True, default=lambda self: self.env.user.company_id)
    insurance_line_ids = fields.One2many('pem.social.insurance.line', 'pem_social_insurance_id', '社保明细', redonly=True, copy=True)
    state = fields.Selection([('unpay', '未缴纳'),
                              ('pay', '已缴纳')],'状态', default='unpay', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', '新建') == '新建':
            vals['name'] = self.env['ir.sequence'].next_by_code('pem.social.insurance') or '/'
        result = super(PemSocialInsurance, self).create(vals)
        return result

    #
    def action_pay(self):
        self.ensure_one()
        if self.state != 'unpay':
            raise UserError('只有在未缴纳状态下才可以提交')
        self.write({'state': 'pay'})
        return True

    @api.depends('insurance_line_ids')
    def compute_total_social_insurance(self):
        for record in self:
            total_company = 0
            total_personal=0
            for line in record.insurance_line_ids:
                total_company += line.company_social_insurance
                total_personal += line.personal_social_insurance
            record.total_company_social_insurance = total_company
            record.total_personal_social_insurance = total_personal

class PemSocialInsuanceLine(models.Model):
    _name = 'pem.social.insurance.line'
    _description = "社保细表"

    user_id = fields.Many2one('res.users', '姓名', default=lambda self: self.env.user, track_visibility='onchange')
    company_social_insurance=fields.Float('公司承担金额',track_visibility='onchange', digits=(10, 3))
    personal_social_insurance = fields.Float('个人承担金额',track_visibility='onchange',digits=(10, 3))
    provided_company_id=fields.Many2one('res.company', '发放公司')
    state = fields.Selection([('unpay', '未缴纳'),
                              ('pay', '已缴纳')], '状态', default='unpay', tracking=True)
    payment_id=fields.Many2one('daily.payment.plan', '日付款计划单号')
    pem_social_insurance_id = fields.Many2one('pem.social.insurance', '社保表单')

