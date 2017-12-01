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
from xadmin import views
from .models import EmailVerifyRecord


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Diomedes"
    site_footer = "Diomedes"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_type", "send_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
