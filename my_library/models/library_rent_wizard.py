from odoo import models,fields,api

class libraryRentWizard(models.TransientModel):
    _name='library.rent.wizart'
    borrower_id=fields.Many2one('res.partner.me',string='Borrower')
    book_ids=fields.Many2many('library.book',string='Books')

    def add_book_rents(self):
        rentModel=self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'borrower_id':wiz.borrower_id.id,
                    'book_id':book.id
                })
