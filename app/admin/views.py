# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from flask import jsonify

from . import admin
from .. import db
from ..decorators import admin_required, permission_required 
from ..models import Permission, User
from .forms import UsereditForm, UseraddForm
from ..appuser import AppUser



@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/user', methods=['GET', 'POST'])
@admin.route('/user/page/<int:page>/', methods=['GET', 'POST'])
@login_required
#@admin_required
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
#@staff_perms_required
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
        message = appuser.add_user(email,username,password)
    data={'message':message}
    return jsonify(data)

@admin.route('/userinfo/', methods=['GET', 'POST'])
@admin.route('/userinfo/<int:uid>/', methods=['GET', 'POST'])
#@staff_perms_required
def userinfo(uid=None):
    if uid is None:
        message = '';
    else :
        appuser=AppUser()
        message=appuser.userinfo(uid)
    return jsonify(message)

@admin.route('/useredit/', methods=['GET', 'POST'])
@admin.route('/useredit/<int:uid>/', methods=['GET', 'POST'])
#@staff_perms_required
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





