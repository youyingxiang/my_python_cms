from flask import Blueprint,jsonify,views,render_template,request,url_for,session,redirect,g
from apps.admin.model import User,Role
from .form import LoginForm,ReSetPwdForm,ReSetEmailForm,UserInfoForm,RoleInfoForm
from .decorator import login_required
from utils import restful,redis
from exts import db,mail
from flask_mail import Message
from utils import menu
import config,string,random
from tasks import send_mail
bp = Blueprint('admin',__name__,url_prefix='/admin')


# 首页
@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')

# 登出
@bp.route('/logout/')
@login_required
def logout():
    del session[config.ADMIN_SESSION_ID]
    session.clear()
    return redirect(url_for('admin.index'))

# 个人简介
@bp.route('/profile/')
@login_required
def profile():
    return render_template('admin/profile.html')

class ReSetpwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('admin/resetpwd.html')
    def post(self):
        form = ReSetPwdForm(request.form)
        if form.validate():
            user = g.u
            input_oldpwd = form.oldpwd.data
            input_newpwd = form.newpwd.data
            if user.check_pwd(input_oldpwd):
                user.password = input_newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error('输入旧密码错误')
        else:
            message = form.get_err_one()
            return restful.params_error(message)
        pass
# 登录
class LoginView(views.MethodView):
    def render(self,message=None):
        return render_template('admin/login.html',message=message)
    def get(self):
        return self.render()
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            u = User.query.filter(User.email == email).first()
            if u and u.check_pwd(password):
                session[config.ADMIN_SESSION_ID] = u.id
                if remember:
                    session.permanent = True
                return redirect(url_for('admin.index'))
            else:
                return self.render(message='密码错误')
        else:
            message = form.get_err_one()
            return self.render(message=message)
# 修改邮箱
class ReSetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('/admin/resetemail.html')
    def post(self):
        form = ReSetEmailForm(request.form)
        if form.validate():
            user = g.u
            user.email = form.email.data
            try:
                db.session.commit()
                return restful.success('恭喜！邮箱修改成功')
            except Exception as e:
                return restful.server_error(str(e))
        else:
            return restful.params_error(form.get_err_one())

@bp.route('/test_email/')
@login_required
def test_email():
    message = Message(subject='测试邮件',html='<h1>这是封测试文件</h1><a href="www.baidu.com">点开连接</a>',recipients=['1365831278@qq.com'])
    try:
        mail.send(message)
        return '发送成功！'
    except Exception as e:
        return str(e)

@bp.route('/email_captche/')
@login_required
def send_email():
    email = request.args.get('email')
    if email:
        strnum = list(string.ascii_letters)
        num = map(lambda x:str(x),range(10))
        strnum.extend(num)
        captche = "".join(random.sample(strnum,6))
        try:
            send_mail.delay('Python论坛邮箱验证码', [email], '您的验证码是：%s' % captche)
            redis.set(email, captche, 120)
            return restful.success('邮件发送成功！')
        except Exception as e:
            return restful.server_error(str(e))
        # message = Message('后台邮箱验证码',body='你的验证码是：'+captche,recipients=[email])
        # try:
        #     mail.send(message)
        #     redis.set(email,captche,120)
        #     return restful.success('邮件发送成功！')
        # except Exception as e:
        #     return restful.server_error(str(e))
        # pass
    else:
        return restful.params_error('请输入邮箱地址！')
# 用户列表
@bp.route('/userlist/')
@login_required
def userlist():
    users = User.query.all()
    return render_template('/admin/userlist.html',data = users)

@bp.route('/userdel/')
def user_del():
    user_id =  request.args.get('id')
    if user_id is None:
        return redirect(url_for('admin.userlist'))
    try:
        userinfo = User.query.get(user_id)
        print(userinfo)
        db.session.delete(userinfo)
        db.session.commit()
        return restful.success('删除成功！')
    except Exception as e:
        return restful.server_error('服务器错误！')

class UserEditView(views.MethodView):
    decorators = [login_required]
    def render(self,data=None,message=None):
        roles = Role.query.all()
        if message is None:
            role = data.roles.first()
            if role:
                data.role = role.id
        return render_template('/admin/useredit.html', data=data,message=message,roles=roles)
    def get(self):
        user_id =  request.args.get('id')
        if user_id is None:
            return redirect(url_for('admin.userlist'))
        userinfo = User.query.get(user_id)
        return self.render(data=userinfo)
    def post(self):
        form = UserInfoForm(request.form)
        if form.validate():
            try:
                user = User.query.get(request.form.get('id'))
                user.email = form.email.data
                user.password = form.password.data
                user.username = form.username.data

                role = Role.query.get(request.form.get('role'))
                user.roles = [role]

                db.session.commit()
                return redirect(url_for('admin.userlist'))
            except Exception as e:
                return  self.render(data=request.form,message=str(e))
        else :
            return self.render(data=request.form,message=form.get_err_one())
        pass

class UserAddView(views.MethodView):
    decorators = [login_required]
    def render(self,data=None,message=None):
        roles = Role.query.all()
        return render_template('/admin/useradd.html',data=data,message=message,roles=roles)
    def get(self):
        return self.render()
    def post(self):
        form = UserInfoForm(request.form)
        if form.validate():
            try:
                u = User(email=form.email.data,password=form.password.data,username=form.username.data)
                role = Role.query.get(request.form.get('role'))
                u.roles = [role]
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('admin.userlist'))
            except Exception as e:
                return  self.render(data=request.form,message=str(e))
        else :
            return self.render(data=request.form,message=form.get_err_one())
        pass


class RoleAddView(views.MethodView):
    decorators = [login_required]
    pris = menu.menu

    def render(self, data=None, message=None):
        if data:
            data = {
                'role_pri':data.getlist('role_pri'),
                'role_type':data.get('role_type'),
                'describe':data.get('describe'),
                'role_name':data.get('role_name')
            }
            pass
        return render_template('/admin/roleadd.html', data=data, message=message,menu=self.pris)

    def get(self):
        return self.render()

    def post(self):
        form = RoleInfoForm(request.form)
        if form.validate():
            try:
                r = Role(
                    role_name=form.role_name.data,
                    role_type=request.form.get('role_type'),
                    describe=form.describe.data,
                    role_pri = request.form.getlist('role_pri')
                )
                print(request.form.getlist('role_pri'))
                db.session.add(r)
                db.session.commit()
                return redirect(url_for('admin.rolelist'))
            except Exception as e:
                return self.render(data=request.form, message=str(e))
        else:
            return self.render(data=request.form, message=form.get_err_one())
        pass

class RoleEditView(views.MethodView):
    decorators = [login_required]
    pris = menu.menu
    def render(self, data=None, message=None):
        if message:
            data = {
                'role_pri':data.getlist('role_pri'),
                'role_type':data.get('role_type'),
                'describe':data.get('describe'),
                'role_name':data.get('role_name')
            }
            pass
        return render_template('/admin/roleedit.html', data=data, message=message,menu=self.pris)

    def get(self):
        role_id = request.args.get('id')
        if role_id is None:
            return redirect(url_for('admin.rolelist'))
        roleinfo = Role.query.get(role_id)
        return self.render(data=roleinfo)

    def post(self):
        form = RoleInfoForm(request.form)
        if form.validate():
            try:
                role= Role.query.get(request.form.get('id'))
                role.role_pri = request.form.getlist('role_pri')
                role.role_name = request.form.get('role_name')
                role.role_type = request.form.get('role_type')
                role.describe  = request.form.get('describe')
                db.session.commit()
                return redirect(url_for('admin.rolelist'))
            except Exception as e:
                return self.render(data=request.form, message=str(e))
        else:
            return self.render(data=request.form, message=form.get_err_one())
        pass

# 角色列表
@bp.route('/rolelist/')
@login_required
def rolelist():
    roles = Role.query.all()
    return render_template('/admin/rolelist.html',data = roles)


@bp.route('/roledel/')
@login_required
def role_del():
    role_id = request.args.get('id')
    if role_id is None:
        return redirect(url_for('admin.rolelist'))
    try:
        roleinfo = Role.query.get(role_id)
        db.session.delete(roleinfo)
        db.session.commit()
        return restful.success('删除成功！')
    except Exception as e:
        return restful.server_error('服务器错误！')

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ReSetpwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ReSetEmailView.as_view('resetemail'))
bp.add_url_rule('/useredit/',view_func=UserEditView.as_view('useredit'))
bp.add_url_rule('/useradd/',view_func=UserAddView.as_view('useradd'))
bp.add_url_rule('/roleadd/',view_func=RoleAddView.as_view('roleadd'))
bp.add_url_rule('/roleedit/',view_func=RoleEditView.as_view('roleedit'))