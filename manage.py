from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from exts import db
from app import app
from apps.admin import model as admin_model

UserModel = admin_model.User


manger = Manager(app)           ###管理
migrate = Migrate(app,db)       ###数据库映射

@manger.option('-u','--username',dest='username')
@manger.option('-e','--email',dest='email')
@manger.option('-p','--password',dest='password')
def add_root(username,email,password):
    u = UserModel(username=username,email=email,password=password)
    db.session.add(u)
    db.session.commit()
    print('用户添加成功！')
manger.add_command('mg',MigrateCommand)

if __name__ == '__main__':
    manger.run()