#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

# !/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import EmailVerifyRecord, GuestProfile


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_type", "send_time"]


class GuestProfileAdmin(object):
    list_display = ['nick_name', 'email', "is_subcribe"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(GuestProfile, GuestProfileAdmin)
