from odoo import models, fields
from odoo import api
import datetime


class WlPlan(models.Model):
    _name = 'wl.plan'
    _description = u'物料表'

    def _default_create_user_id(self):
        return self.env.uid

    name = fields.Char(string=u"物料名称")
    date = fields.Date(string=u"创建日期", default=fields.Date.today)
    product_id = fields.Many2one('wl.product.type', string="来源")

    product_amount = fields.Integer(string="产品数量", compute='compute_product_count', copy=False)
    start_time = fields.Datetime(string="进料时间")
    end_time = fields.Datetime(string="使用时间")
    store_time = fields.Float(string="存料时间", compute='compute_store_time', store=True)
    remarks = fields.Text(string=u"备注")

    wl_bom_lines = fields.One2many('wl.bom', 'wl_plan_id', string='物料成分')

    @api.model
    def compute_product_count(self):
        amount = self.env['wl.product.type'].sudo().search([('product_type', '=', self.product_type)])
        self.update({'product_amount': len(amount)})

    @api.depends('start_time', "end_time")
    def compute_store_time(self):
        for order in self:
            if order.start_time and order.end_time:
                start_datetim = datetime.datetime.strptime(str(order.start_time), '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.datetime.strptime(str(order.end_time), '%Y-%m-%d %H:%M:%S')
                time_delta = end_datetime - start_datetim
                order.store_time = round(time_delta.total_seconds() / 3600, 2)


class WlBom(models.Model):
    _name = 'wl.bom'

    name = fields.Char('成分')
    amount = fields.Float('数量')
    wl_plan_id = fields.Many2one('bom.plan', string='物料表')
