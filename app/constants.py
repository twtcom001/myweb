#!/usr/bin/python
#coding=utf-8

import re


# 邮箱正则
EMAIL_PATTERN = re.compile(
    r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)

# Unicode字符, 数字、字母_-中文
UNICODE_PATTERN = r'^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$'
# @用户
AT_USER_PATTEN = r'@(?P<user>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)'
# 话题
TOPIC_PATTEN = r'#(?P<topic>[a-zA-Z0-9_\-\u4e00-\u9fa5]+)#'
