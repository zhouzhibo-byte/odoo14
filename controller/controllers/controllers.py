# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Main(http.Controller):
    @http.route('/controllers/books', type='http', auth='none')
    def books(self):
        print('222222222222')
        books = request.env['library.book1'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/controllers/books/json', type='json', auth='none')
    def books_json(self):
        records = request.env['library.book1'].sudo().search([])
        return records.read(['name'])