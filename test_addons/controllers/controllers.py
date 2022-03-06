# -*- coding: utf-8 -*-
# from odoo import http


# class TestAddons(http.Controller):
#     @http.route('/test_addons/test_addons/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_addons/test_addons/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_addons.listing', {
#             'root': '/test_addons/test_addons',
#             'objects': http.request.env['test_addons.test_addons'].search([]),
#         })

#     @http.route('/test_addons/test_addons/objects/<model("test_addons.test_addons"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_addons.object', {
#             'object': obj
#         })
