#coding: utf-8
from datetime import datetime
from models import Logs
from . import db

def insert_log(email,level,comment):
        logs = Logs(email=email, level=level, op_time=datetime.now(), comment=comment)
        db.session.add(logs)
        db.session.commit()
