#!/usr/bin/env python
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db

	
# python manage.py db init
# python manage.py db migrate
app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':

	app.run(debug=True, use_reloader=False)