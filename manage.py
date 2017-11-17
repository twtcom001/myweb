#!/usr/bin/env python
#coding: utf-8
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User
from flask.ext.uploads import UploadSet, configure_uploads

# 设置环境 默认default 未开发环境
# FLASK_CONFIG = ProdConfig
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 增加db 初始化功能
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# flask.ext.uploads  模块设置
upfile = UploadSet('FILE')      #名字最好取大写，因为config里面都是要求大写，这样容易匹配  
configure_uploads(app, upfile)  #再把app和这个upfile这个上传组给绑定

# shell模式增加字典
def make_shell_context():
    return dict(db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))

# 初始化数据
@manager.command
def deploy():
	from app.models import User, Role
	# 初始化权限
	Role.insert_roles()
	#初始化管理员账号
	User.insert_admin(email='106640085@qq.com', username='xuhonglin', password='xuhonglin', role_id=1)


if __name__ == '__main__':

	manager.run()