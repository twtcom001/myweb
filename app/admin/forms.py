
# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional


class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])

class UsereditForm(Form):
    """ 用户信息表单 """
    nickname = StringField(label='电子邮件', validators=[DataRequired(), Length(1, 64), Email()],
        description="请输入电子邮件",
        render_kw={ "class": "form-control"})
    is_valid = SelectField(label='状态', validators=[DataRequired()],
        render_kw={ "class": "form-control"})
    password = PasswordField(label='密码', validators=[Optional()],
        description="请输入密码",
        render_kw={"class": "form-control"})
    submit = SubmitField('保存信息', render_kw={
            'class': 'btn btn-info'})