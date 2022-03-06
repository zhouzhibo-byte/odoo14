from odoo import models,fields,api

class child(models.Model):
    _inherit='parent'

    num_people=fields.Integer(string='人数')
    authored_book_ids=fields.Many2many('library.book',string='Authored Book')
    count_books=fields.Integer('Number of Authored Book',compute='_coumpute_count_books',store=True)
    type=fields.Char(string='类型')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books=len(r.authored_book_ids)