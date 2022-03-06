# -*- coding: utf-8 -*-
# from odoo import http


# class ButtonTest(http.Controller):
#     @http.route('/button_test/button_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/button_test/button_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('button_test.listing', {
#             'root': '/button_test/button_test',
#             'objects': http.request.env['button_test.button_test'].search([]),
#         })

#     @http.route('/button_test/button_test/objects/<model("button_test.button_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('button_test.object', {
#             'object': obj
#         })
