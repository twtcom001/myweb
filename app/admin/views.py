# coding:utf-8
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from flask import jsonify

from . import admin
from .. import db, upfile
from ..decorators import admin_required, permission_required
from ..models import Permission, User, Logs, Plants
from .forms import UsereditForm, UseraddForm, UploadForm
from ..appclass import AppUser, insert_log, batch_insert


@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/log', methods=['GET', 'POST'])
@admin.route('/log/page/<int:page>/', methods=['GET', 'POST'])
@login_required
@admin_required
def log(page=None):

    if page is None:
        page = 1
    page_data = Logs.query.filter(id>0).paginate(
        page=page, per_page=50)

    return render_template('admin/log.html', page_data=page_data)

@admin.route('/user', methods=['GET', 'POST'])
@admin.route('/user/page/<int:page>/', methods=['GET', 'POST'])
@login_required
@admin_required
def user(page=None):
    editform = UsereditForm()
    addform = UseraddForm()
    if page is None:
        page = 1
    page_data = User.query.filter(id>0).paginate(
        page=page, per_page=3)

    return render_template('admin/user.html', page_data=page_data, form1=editform, form=addform)

#ajax 加载

@admin.route('/useradd', methods=['GET', 'POST'])
@login_required
@admin_required
def useradd():
    message = ''
    appuser=AppUser()
    #接收username，没有默认为''
    email = request.values.get('email', '')
    if email is not '' :
        message = appuser.validate_email(email)
    username = request.values.get('username', '')
    if username is not '' :
        message = appuser.validate_username(username)
    password = request.values.get('password', '')
    if password is not '' :
        message = appuser.validate_password(password)
    if username and email and password:
        message = appuser.useradd(email,username,password)
        insert_log(current_user.email,1,unicode(message) )
    data={'message':message}
    return jsonify(data)

@admin.route('/userinfo/', methods=['GET', 'POST'])
@admin.route('/userinfo/<int:uid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def userinfo(uid=None):
    if uid is None:
        message = '';
    else :
        appuser=AppUser()
        message=appuser.userinfo(uid)
    return jsonify(message)

@admin.route('/useredit/', methods=['GET', 'POST'])
@admin.route('/useredit/<int:uid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def useredit(uid=None):
    if uid is None:
        message = '';
    else :
        appuser=AppUser()
        username = request.values.get('username', '')
        password = request.values.get('password', '')
        #uid = request.values.get('uid', '')
    
        message=appuser.usersave(uid, username, password)
    data={'message':message}
    return jsonify(data)

@admin.route('/userdel/', methods=['GET', 'POST'])
@admin.route('/userdel/<int:uid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def userdel(uid=None):
    if uid is None:
        message = '';
    else :
        appuser=AppUser()
        message=appuser.userdel(uid)
        insert_log(current_user.email,1,unicode(message) )
    data={'message':message}
    return jsonify(data)


@admin.route('/plants/', methods=['POST', 'GET'])
@admin.route('/plants/page/<int:page>/', methods=['GET', 'POST'])
def plants(page=1):
    filename = ''
    form = UploadForm()
    if request.method == 'POST' and 'file' in request.files:
        filename = upfile.save(request.files['file'])
        batch_insert(filename)
    if page is None:
        page = 1
    page_data = Plants.query.filter(id>0).paginate(
        page=page, per_page=50)    

    return render_template('admin/plants.html', page_data=page_data, form=form)




