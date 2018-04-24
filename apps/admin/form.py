from wtforms import StringField,IntegerField
from ..from_base import FormBase
from wtforms.validators import email,InputRequired,Length,EqualTo,ValidationError
from flask import g
from utils import redis
from .model import User
class LoginForm(FormBase):
    email = StringField(validators=[email(message='邮箱格式不正确'),InputRequired(message='邮箱输入不能为空')])
    password = StringField(validators=[InputRequired(message='密码不能为空'),Length(max=8,min=6,message='密码长度必须为6-8位')])
    remember = IntegerField()
class ReSetPwdForm(FormBase):
    oldpwd = StringField(validators=[InputRequired(message='旧密码不能为空'), Length(max=8, min=6, message='旧密码长度必须为6-8位')])
    newpwd = StringField(validators=[InputRequired(message='新密码不能为空'),Length(max=8,min=6,message='新密码长度必须为6-8位')])
    renewpwd = StringField(validators=[EqualTo('newpwd',message='两次密码不一致')])

class UserInfoForm(FormBase):
    email = StringField(validators=[email(message='邮箱格式不正确'), InputRequired(message='邮箱输入不能为空')])
    username = StringField(validators=[InputRequired(message='用户姓名不能为空'),Length(max=20,min=2,message='用户名称长度2-20位')])
    password = StringField(validators=[InputRequired(message='密码不能为空'), Length(max=8, min=6, message='密码长度必须为6-8位')])
    renewpwd = StringField(validators=[EqualTo('password', message='两次密码不一致')])

class ReSetEmailForm(FormBase):
    email = StringField(validators=[email(message='邮箱格式不正确'), InputRequired(message='邮箱输入不能为空')])
    captche = StringField(validators=[Length(min=6,max=6,message='请输入正确验证码长度')])
    def validate_email(self,field):
        email = field.data
        if email == g.u.email:
            raise ValidationError('修改邮箱和当前邮箱重复！')
        is_exis = User.query.filter(User.email == email).count()
        if is_exis:
            print(is_exis);
            raise ValidationError('修改邮箱已经存在！')
    def validate_captche(self,field):
        captche = field.data
        try:
            redis_captche = redis.get(self.email.data)
        except Exception as e:
            raise ValidationError(str(e))
        if not redis_captche or redis_captche.decode('utf-8').lower() != captche.lower():
            raise ValidationError('验证码输入不正确！')

class RoleInfoForm(FormBase):
    role_name = StringField(validators=[InputRequired(message='角色名称不能为空'), Length(max=20, min=2, message='角色名称长度2-20位')])
    describe = StringField(validators=[Length(max=1000, message='角色描述太长')])

