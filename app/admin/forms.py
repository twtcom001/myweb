
# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional


class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])

class UsereditForm(Form):
    """ 用户信息表单 """
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[Optional()])
    submit = SubmitField('保存信息')

class UseraddForm(Form):
    """ 用户注册 """
    email = StringField(label="个人邮箱", validators=[DataRequired()],
        render_kw={"required": 'required', "placeholder": "请输入个人邮箱", "class": "form-control"},
        description="输入用用户邮箱注册")

    username = StringField(label="用户名", validators=[DataRequired()],
        render_kw={"required": 'required', "placeholder": "请输入用户名", "class": "form-control"},
        description="输入用户昵称")
    password = PasswordField('密码', validators=[DataRequired("请输入密码")], 
        render_kw={"required": 'required', "class": "form-control"}
        )