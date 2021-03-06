# coding: utf-8
from datetime import datetime

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm
from ..app import insert_log

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            user.last_login = datetime.now()
            db.session.add(user)
            db.session.commit()
            insert_log(form.email.data,1,u'%s login sucess' % form.email.data)
            flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
            return redirect(request.args.get('next') or url_for('admin.index'))
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))