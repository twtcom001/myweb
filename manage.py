#!/usr/bin/env python
#coding: utf-8
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User

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

# shell模式增加字典
def make_shell_context():
    return dict(db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))

# 初始化数据
@manager.command
def deploy():
	from app.models import User
	User.insert_admin(email='106640085@qq.com', username='xuhonglin', password='xuhonglin')


if __name__ == '__main__':

	manager.run()