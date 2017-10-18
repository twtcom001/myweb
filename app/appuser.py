#!/usr/bin/python
#coding=utf-8

import re
from datetime import datetime
from flask import render_template, redirect, flash, url_for, request, abort
from flask import jsonify

#from app import app, login_manager, db
from models import User
from . import db, constants
#from app.constants import PermsEnum, ValidEnum

class AppUser(object):
    validate=True
    def validate_password(self,password):
        if len(password) <= 6:
            self.validate=False
            return "密码必须是6位以上"
        return "密码符合标准"

    def validate_email(self,email):
        email = email.lower()
        # 判断改用户名是否已经存在
        user = User.query.filter_by(email=email).first()
        if user is not None:
            self.validate=False
            return "该用户已经注册"
        # 用户名必须是邮箱
        if not re.search(constants.EMAIL_PATTERN, email):
            self.validate=False
            return '请用邮箱注册'
        return "用户名符合标准"

    def validate_username(self,username):
        # 判断改用户名是否已经存在
        user = User.query.filter_by(username=username).first()
        if user is not None:
            self.validate=False
            return "该昵称已使用"
    
    def userinfo(self,uid):
        user = User.query.filter_by(id=uid).first()
        if user.is_valid :
        	is_valid = "Enable"
        else:
        	is_valid = "Disable"
        data = { 'uid':user.id,'username':user.username,'is_valid':is_valid}
        return data
    
    def usersave(self,uid,username,password):
    	if self.validate:
            user = User.query.filter_by(id=uid).first()
            if user.username != username:
                user.username = username
            #if is_valid == 'Enable':
            #    user.is_valid = True
            #else:
            #    user.is_valid = False
            if password != "":
                """更新密码"""
                user.password = password
            db.session.commit()
        return "修改用户成功"



    def add_user(self,email,username,password):
        if self.validate:
            user = User(
            email=email,
            username=username,
            )
            # 设置用户的密码
            user.password=password
            db.session.add(user)
            db.session.commit()
            return "新增用户成功"         
        else:
            return "新增用户失败"

