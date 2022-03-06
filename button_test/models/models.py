# -*- coding: utf-8 -*-

from odoo import models, fields, api


class button_test(models.Model):
    _name = 'button.test'
    _description = 'button_test.button_test'

    name = fields.Char(string="按钮")
    state = fields.Selection([('origin','普通'),('sanjiao','三角'),('yuanxing','圆形')], default="origin",string="状态")


    def set_origin(self):
        self.write({'state':'origin'})

    def set_sanjiao(self):
        # self.state='sanjiao'
        self.write({'state':'sanjiao'})

    def set_yuanxing(self):
        self.write({'state':'yuanxing'})


