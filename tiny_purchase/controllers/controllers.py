# -*- coding: utf-8 -*-
import json
from odoo.http import Controller
from odoo import  http






# class TinyPurchase(Controller):
#     @api_route('/tiny_purchase/tiny_purchase/' ,type='pure_json',auth='public')
#     def index(self, **kw):
#
#         return {'123':'1231'}



#     @http.route('/tiny_purchase/tiny_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tiny_purchase.listing', {
#             'root': '/tiny_purchase/tiny_purchase',
#             'objects': http.request.env['tiny_purchase.tiny_purchase'].search([]),
#         })

#     @http.route('/tiny_purchase/tiny_purchase/objects/<model("tiny_purchase.tiny_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tiny_purchase.object', {
#             'object': obj
#         })
