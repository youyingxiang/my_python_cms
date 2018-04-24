from flask import redirect,url_for,session,request,g
from functools import wraps
import config

# session 登录检测
def login_required(func):
    @wraps(func)
    def check_session(*args,**kwargs):
        if config.ADMIN_SESSION_ID in session:
            path = request.path
            if hooks_auth(path) == False:
                return redirect(url_for('admin.index'))
            else:
                return func(*args,*kwargs)
        else:
            return redirect(url_for('admin.login'))
    return check_session

#     path = request.path
#     hooks_auth(path)
def hooks_auth(path):
    have_auth = False
    # 不是登录的路由
    if g.u:
        if g.u.roles.first().role_type == 1:
            have_auth = True
        elif str(path) in ['/admin/', '/admin', '/admin/logout/','/admin/logout/']:
            have_auth = True
        else:
            pri = g.u.roles.first().role_pri_path
            path2 = path[0:-1]
            if path2 in pri:
                have_auth = True
                pass
            if path in pri:
                have_auth = True
                pass
        return have_auth
