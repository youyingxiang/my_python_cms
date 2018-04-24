from flask import jsonify

class HttpCode(object):
    success = 200
    unautherror = 401
    paramserror = 400
    servererror = 500

def restful_result(code,message,data):
    return jsonify({"code":code,"message":message,"data":data or {}})

def success(message="",data=None):
    return restful_result(code=HttpCode.success,message=message or '请求成功！',data=data)

def unauth_error(message=""):
    return restful_result(code=HttpCode.unautherror,message=message or '没有权限！',data=None)

def params_error(message=""):
    return restful_result(code=HttpCode.paramserror,message=message or '输入参数错误！',data=None)

def server_error(message=""):
    return restful_result(code=HttpCode.servererror,message=message or '服务器内部错误',data=None)