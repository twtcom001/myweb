# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import admin
from .. import db
from ..decorators import admin_required, permission_required 
from ..models import Permission, User
from .forms import UsereditForm



@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/user', methods=['GET', 'POST'])
@admin.route('/user/page/<int:page>/', methods=['GET', 'POST'])
@login_required
#@admin_required
def user(page=None):
    if page is None:
        page = 1
    page_data = User.query.filter(id>0).paginate(
        page=page, per_page=3)

    return render_template('admin/user.html', page_data=page_data)

@admin.route('/useredit', methods=['GET', 'POST'])
@admin.route('/useredit/<int:uid>/', methods=['GET', 'POST'])
#@staff_perms_required
def useredit(uid=None):
    form = UsereditForm()
    if uid is None:
        return redirect(url_for('admin.user'))
    user = User.query.filter_by(id=1).first()
    if form.validate_on_submit():
        data = form.data
        if user.email != data['email']:
            user.email=data['email']
        if data['is_valid'] == 'Enable':
            user.is_valid = True
        else:
            user.is_valid = False
        if data['password'] != "":
            user.set_password(data['password'])
        db.session.commit()
        return redirect(url_for('admin.user'))
    else:
        if user.is_valid:
            form.is_valid.data = 'Enable'
        else:
            form.is_valid.data = 'Disable'      
    return render_template("admin/useredit.html", form = form, user = user )




