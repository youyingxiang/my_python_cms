from flask import session,g,request
from .view import bp
from .model import User
import config

# 请求之前钩子函数
@bp.before_request
def before_request():
    if config.ADMIN_SESSION_ID in session:
        uid = session.get(config.ADMIN_SESSION_ID)
        u = User.query.get(uid)
        if u:
            g.u = u
    path = request.path
    hooks_auth(path)
def hooks_auth(path):
    # 不是登录的路由
    if path != '/admin/login' and path != '/admin/login/':
        pass
    else:
        pri = g.u.roles.first().role_pri_path
