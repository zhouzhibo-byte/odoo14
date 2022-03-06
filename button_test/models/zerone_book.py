from odoo import models,fields,api


class ZeroneBook(models.Model):
    _name = "zerone.book2"
    _description = "Zerone Books"

    name = fields.Char(string="图书名称", required=True)
    code = fields.Char(string="图书编号", required=True)
    state = fields.Selection([('draft', '未被借出'), ('rent', '已经借出'), ('return', '已经归还')],
                             default='draft', string="状态")

    def action_bjl(self):
        self.state = 'draft'

    def action_jc(self):
        self.state = 'rent'

    def action_gh(self):
        self.state = 'return'

    def action_xbhl(self):
        self.state = 'rent'
