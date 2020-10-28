# -*- coding: utf-8 -*-
import json

from odoo.exceptions import AccessDenied
from odoo.http import Controller, Response, HttpRequest
from odoo import http
from odoo import fields
import traceback

from odoo.tools import date_utils


# def response(result):
#     mime = 'application/json'
#     body = json.dumps(result, default=date_utils.json_default)
#     return Response(body, 200, headers=[('Content-Type', mime), ('Content-Length', len(body))])
#
#
# def context(f):
#     '''
#     设置环境变量和登录
#     '''
#
#     def wrapper(self, request, *args, **kw):
#
#         try:
#             authorization_header = request.httprequest.headers.get('Authorization')
#             if not authorization_header:
#                 raise ApiException(-1, '没找到token请求头')
#             token = authorization_header.split(' ')[1]
#             user = request.env['res.users'].sudo().search(
#                 [('token', '=', token), ('expire_time', '>', fields.datetime.now())])
#             if not user:
#                 raise ApiException(-1, 'token过期或者错误')
#             user.refresh_expire()
#             query = request.env['base'].with_user(user)
#             query.env.uid = user.id
#
#             varnames = f.__code__.co_varnames
#             if (len(varnames) >= 2 and varnames[1] in ['req', 'request']):
#                 result = f(self, request, query, *args, **kw)
#                 if isinstance(request, HttpRequest) and not isinstance(result, Response):
#                     return response(result)
#                 return result
#             else:
#                 result = f(self, query, *args, **kw)
#                 if isinstance(request, HttpRequest) and not isinstance(result, Response):
#                     return response(result)
#                 return result
#
#         except ApiException as e1:
#             return {'code': e1.code, 'message': e1.message}
#         except Exception as e2:
#             return {'code': -1, 'message': traceback.format_exc(e2)}
#
#     wrapper.__name__ = f.__name__
#     return wrapper
#
#
# http.context = context


class BaseController(Controller):
    @http.route('/user/login', auth='public', csrf=False, cors='*')
    def user_login(self, request, **kw):
        username = kw.get('username')
        password = kw.get('password')
        user = request.env['res.users'].sudo().search([('login', '=', username)])
        if not user:
            return {'code': -1, 'message': '用户名不存在!'}
        try:
            user.with_user(user)
            user.env.uid = user.id
            user._check_credentials(password)
        except AccessDenied:
            return {'code': -1, 'message': '密码认证失败!'}
        user.refresh_token()
        return {
            'code': 0,
            'token': user.token
        }

    @http.route("/hello",type='json',auth='user',jsonrpc=False, csrf=False, cors='*')
    def hello(self,request,**kw):
        return {"hello":"hello"}

    # @api_route('/user/info', type='pure_json', methods=['GET'])

    @http.route("/user/info", type='http', auth='user', jsonrpc=False, csrf=False, cors='*')
    def user_info(self, req, **kw):
        user = req.env.user
        result= {
            'code': 0,
            'city': user.city,
            'company_name': user.company_name,
            'contact_address': user.contact_address,
            'display_name': user.display_name,
            'email': user.email,
            'image': user.image_512,
            'lang': user.lang,
            'login_name': user.login,
            'phone': user.phone,
            'tz': user.tz,
            'tz_offset': user.tz_offset
        }
        return http.dict_response(result)

    # @http.route('/tiny_base/tiny_base/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('tiny_base.listing', {
#             'root': '/tiny_base/tiny_base',
#             'objects': http.request.env['tiny_base.tiny_base'].search([]),
#         })

#     @http.route('/tiny_base/tiny_base/objects/<model("tiny_base.tiny_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tiny_base.object', {
#             'object': obj
#         })
