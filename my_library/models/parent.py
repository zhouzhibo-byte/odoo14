from odoo import models,api,fields

class parent(models.Model):
    _name='parent'

    name=fields.Char(string='科室')
    parent_id=fields.Integer(string="编号")
    type=fields.Char(string="类型")