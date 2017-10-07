# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import admin
from .. import db


@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/index.html')