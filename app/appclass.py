#!/usr/bin/python
#coding=utf-8

import re
from datetime import datetime
import xlrd
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask import render_template, redirect, flash, url_for, request, abort
from flask import jsonify
from models import User, Logs, Plants, Introduce
from . import db, constants


def batch_insert(filename):
    workbook = xlrd.open_workbook(basedir+'\static\upload\\'+filename)
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    for i in range(1,sheet.nrows):
        if i > 0:
            if not Plants.query.filter_by(local_id = int(sheet.row_values(i)[0])).one_or_none() :
                plants = Plants(local_id = int(sheet.row_values(i)[0]),
                familia = sheet.row_values(i)[1],
                genus = sheet.row_values(i)[2],
                genus_id = sheet.row_values(i)[3],
                icbn_name = sheet.row_values(i)[4],
                chinese_name = sheet.row_values(i)[5],
                info_url = sheet.row_values(i)[9],
                comment = sheet.row_values(i)[11])
                db.session.add(plants)
                db.session.commit()
            introduce = Introduce(introduce_id = sheet.row_values(i)[6],
            introduce_from = sheet.row_values(i)[8],
            introduce_price = sheet.row_values(i)[7],
            introduce_date = sheet.row_values(i)[10],
            palnts_id = int(sheet.row_values(i)[0]))
            db.session.add(introduce)
            db.session.commit()

def insert_log(email,level,comment):
        logs = Logs(email=email, level=level, op_time=datetime.now(), comment=comment)
        db.session.add(logs)
        db.session.commit()

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



    def useradd(self,email,username,password):
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

    def userdel(self,uid):
        if ( uid == 1 ):
            return "管理员禁止删除!"
        else:
            user = User.query.filter_by(id=uid).first()
            db.session.delete(user)
            db.session.commit()
            return "删除用户成功!"

