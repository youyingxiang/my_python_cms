from exts import db
from werkzeug.security import check_password_hash,generate_password_hash
from utils import menu
import time


role_user = db.Table(
    'role_user',
    db.Column('role_id',db.Integer,db.ForeignKey('role.id',ondelete = 'CASCADE'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),primary_key=True)
)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), nullable=False,unique=True)
    username = db.Column(db.String(100), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    _create_time = db.Column(db.Integer,nullable=False,default=time.time())

    def __init__(self,password,email,username):
        self.password = password
        self.email = email
        self.username = username
    # 获取密码
    @property
    def password(self):
        return self._password

    # 密码加密
    @password.setter
    def password(self,input_password):
        self._password = generate_password_hash(input_password)

    # 检测密码
    def check_pwd(self,input_password):
        res = check_password_hash(self._password,input_password)
        return res

    # 获取创建时间
    @property
    def create_time(self):
        create_time_value = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self._create_time))
        return create_time_value

    # def __repr__(self):
    #     return "<User:id=%s email=%s password=%s username=%s date=%s>" % (self.id,self.email,
    #                                                                       self.password,self.username,self.create_time)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_type = db.Column(db.SmallInteger, nullable=False)
    describe  = db.Column(db.Text,nullable=True)
    _role_pri = db.Column(db.Text,nullable=True)
    _create_time = db.Column(db.Integer, nullable=False, default=time.time())
    users = db.relationship('User', secondary=role_user, backref=db.backref('roles',lazy='dynamic'))
    # 获取创建时间
    @property
    def create_time(self):
        create_time_value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._create_time))
        return create_time_value

    # 获取权限值
    @property
    def role_pri(self):
        pris = self._role_pri.split(",")
        return pris

    @role_pri.setter
    def role_pri(self, input_role_pri):
        self._role_pri = ",".join(input_role_pri)

    @property
    def role_pri_name(self):
        pris = self._role_pri.split(",")
        pris_name = []
        for v in menu.menu:
            if str(v.get('id')) in pris:
                pris_name.append(v.get('pri_name'))
            if v.get('child'):
                for vv in v.get('child'):
                    if str(vv.get('id')) in pris:
                        pris_name.append(vv.get('pri_name'))
                    if vv.get('child'):
                        for vvv in vv.get('child'):
                            if str(vvv.get('id')) in pris:
                                pris_name.append(vvv.get('pri_name'))
        return ",".join(pris_name)

    @property
    def role_pri_path(self):
        pris = self._role_pri.split(",")
        pri_path = []
        for v in menu.menu:
            if str(v.get('id')) in pris:
                if v.get('action_name'):
                    path = '/'+v.get('url_prefix')+'/'+ v.get('action_name')
                else:
                    path = '/' + v.get('url_prefix')
                pri_path.append(path)
            if v.get('child'):
                for vv in v.get('child'):
                    if str(vv.get('id')) in pris:
                        if vv.get('action_name'):
                            path = '/' + vv.get('url_prefix') + '/' + vv.get('action_name')
                        else:
                            path = '/' + vv.get('url_prefix')
                        pri_path.append(path)
                    if vv.get('child'):
                        for vvv in vv.get('child'):
                            if str(vvv.get('id')) in pris:
                                if vv.get('action_name'):
                                    path = '/' + vvv.get('url_prefix') + '/' + vvv.get('action_name')
                                else:
                                    path = '/' + vvv.get('url_prefix')
                                    pri_path.append(path)
        return ",".join(pri_path)






