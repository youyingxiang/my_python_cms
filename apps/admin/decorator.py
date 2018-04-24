from flask import redirect,url_for,session
from functools import wraps
import config

# session 登录检测
def login_required(func):
    @wraps(func)
    def check_session(*args,**kwargs):
        if config.ADMIN_SESSION_ID in session:
            return func(*args,*kwargs)
        else:
            return redirect(url_for('admin.login'))
    return check_session
