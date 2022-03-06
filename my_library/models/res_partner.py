from odoo import models,fields

class ResPartner(models.Model):
    _name='res.partner.me'

    name=fields.Char(string='出版社名称')
    author=fields.Char(string="出版社签约作者")
    city=fields.Char(string='城市')