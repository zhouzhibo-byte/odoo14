# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class PemAccumulation(models.Model):
    _name = 'pem.accumulation.fund'
    _description = "公积金"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('公基金编号', required=True, readonly=True, index=True, copy=False, default='新建')
    user_name=fields.Many2one('res.users','创建人',default=lambda self: self.env.user, track_visibility='onchange')
    date = fields.Date('创建时间', readonly=True, copy=False, default=fields.Date.today)
    total_company_commitment_amount=fields.Float('公司应付公积金合计',compute='compute_total_commitment_amount', store=True,track_visibility='always', digits=(10, 3))
    total_personal_commitment_amount=fields.Float('个人应付公积金合计',compute='compute_total_commitment_amount', store=True,track_visibility='always', digits=(10, 3))
    company_id = fields.Many2one('res.company', '公司', readonly=True, default=lambda self: self.env.user.company_id)
    pem_accumulation_fund_line_ids = fields.One2many('pem.accumulation.fund.line', 'pem_accumulation_fund_id', '个人所得税明细', redonly=True,
                                   copy=True)
    state = fields.Selection([('unpay', '未缴纳'),
                              ('pay', '已缴纳')],'状态', default='unpay', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', '新建') == '新建':
            vals['name'] = self.env['ir.sequence'].next_by_code('pem.accumulation.fund') or '/'
        result = super(PemAccumulation, self).create(vals)
        return result

    #
    def action_pay(self):
        self.ensure_one()
        if self.state != 'unpay':
            raise UserError('只有在未缴纳状态下才可以提交')
        self.write({'state': 'pay'})
        return True

    @api.depends('pem_accumulation_fund_line_ids')
    def compute_total_commitment_amount(self):
        for record in self:
            total_company_money = 0
            total_personal_money=0
            for line in record.pem_accumulation_fund_line_ids:
                total_company_money += line.company_commitment_amount
                total_personal_money += line.personal_commitment_amount
            record.total_company_commitment_amount = total_company_money
            record.total_personal_commitment_amount = total_personal_money

class PemAccumulationFundLine(models.Model):
    _name = 'pem.accumulation.fund.line'
    _description = "公积金明细表"

    user_id = fields.Many2one('res.users', '姓名', default=lambda self: self.env.user, track_visibility='onchange')
    company_commitment_amount=fields.Float('公司承担金额',track_visibility='onchange', digits=(10, 3))
    personal_commitment_amount = fields.Float('个人承担金额',track_visibility='onchange',digits=(10, 3))
    provided_company_id=fields.Many2one('res.company', '发放公司')
    state = fields.Selection([('unpay', '未缴纳'),
                              ('pay', '已缴纳')], '状态', default='unpay', tracking=True)
    payment_id=fields.Many2one('daily.payment.plan', '日付款计划单号')
    pem_accumulation_fund_id = fields.Many2one('pem.accumulation.fund', '公积金表单')

