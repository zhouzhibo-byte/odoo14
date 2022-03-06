from odoo import models, fields


class WlProductType(models.Model):
    _name = "wl.product.type"
    _description = '产品类型表'

    name = fields.Char(string="产品名称")
    come_place = fields.Char(string="生产地")
    wl_ids = fields.One2many(comodel_name="wl.plan", inverse_name='name', string="物料类型")
    wl_color_ids = fields.Many2many("wl.plan", string="物料颜色")
    remarks = fields.Char(string="备注信息")
