# -*- coding: utf-8 -*-
# from odoo import http


# class ZeroneBook(http.Controller):
#     @http.route('/zerone_book/zerone_book/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zerone_book/zerone_book/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zerone_book.listing', {
#             'root': '/zerone_book/zerone_book',
#             'objects': http.request.env['zerone_book.zerone_book'].search([]),
#         })

#     @http.route('/zerone_book/zerone_book/objects/<model("zerone_book.zerone_book"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zerone_book.object', {
#             'object': obj
#         })
