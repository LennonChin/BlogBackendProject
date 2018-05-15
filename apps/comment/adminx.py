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
from django import forms
from .models import CommentInfo, CommentDetail
from pagedown.widgets import AdminPagedownWidget


class CommentDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = CommentDetail
        fields = '__all__'


class CommentDetailAdmin(object):
    form = CommentDetailForm
    exclude = ['formatted_content']
    model = CommentDetail
    extra = 0


class CommentInfoAdmin(object):
    list_display = ['post', 'author', 'reply_to_author', 'reply_to_comment', 'add_time']
    search_fields = ['post']

    inlines = [CommentDetailAdmin]


xadmin.site.register(CommentInfo, CommentInfoAdmin)