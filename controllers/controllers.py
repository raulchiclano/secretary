# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/secretary(http.Controller):
#     @http.route('//mnt/extra-addons/secretary//mnt/extra-addons/secretary', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/secretary//mnt/extra-addons/secretary/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/secretary.listing', {
#             'root': '//mnt/extra-addons/secretary//mnt/extra-addons/secretary',
#             'objects': http.request.env['/mnt/extra-addons/secretary./mnt/extra-addons/secretary'].search([]),
#         })

#     @http.route('//mnt/extra-addons/secretary//mnt/extra-addons/secretary/objects/<model("/mnt/extra-addons/secretary./mnt/extra-addons/secretary"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/secretary.object', {
#             'object': obj
#         })
