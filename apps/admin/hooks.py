from flask import session,g,request
from .view import bp
from .model import User
import config
from utils import menu

# 请求之前钩子函数
@bp.before_request
def before_request():
    if config.ADMIN_SESSION_ID in session:
        uid = session.get(config.ADMIN_SESSION_ID)
        u = User.query.get(uid)
        if u:
            g.u = u

@bp.context_processor
def menu_c():
    m = menu.menu
    if config.ADMIN_SESSION_ID in session:
        if g.u.roles.first().role_type == 1:
            have_auth = 'all'
        else:
            have_auth = g.u.roles.first().role_pri
    else:
        have_auth = []
    return {'menu_cd':m,'have_auth':have_auth}
