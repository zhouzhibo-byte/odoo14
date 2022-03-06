# -*- coding: utf-8 -*-
from odoo import models, fields,api


class LibraryBook(models.Model):
    _name = 'library.book1'
    _description = 'Library Book'
    _order = 'date_release desc, name'

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection([('txrub', '填写入职表单'),
                              ('itwh', 'IT维护'),
                              ('wyqr', '文员确认')], '状态', default='txrub', index=True, copy=False,
                             track_visibility='onchange')

    def get_portal_url(self):
        portal_link = "%s/?db=%s" % (
        self.env['ir.config_parameter'].sudo().get_param('web.base.url'), self.env.cr.dbname)
        return portal_link

    def preview_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    @api.onchange('state')
    def get_t(self):
        print('11111111111')
        print(self.get_portal_url())
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def get_stock_file(self):
        return {'type': 'ir.actions.act_url',
                'url': '/controllers/books',
                'target': 'self', }
    #
    # def book_return(self):
    #     self.ensure_one()
    #     self.write({
    #         'state': 'returned'
    #     })