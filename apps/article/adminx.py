#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

from django import forms

from .models import ArticleInfo, ArticleDetail
from material.models import PostTag
from pagedown.widgets import AdminPagedownWidget


class ArticleDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = ArticleDetail
        fields = '__all__'


class ArticleDetailAdmin(object):
    form = ArticleDetailForm
    exclude = ['formatted_content']
    model = ArticleDetail
    extra = 1


class ArticleInfoAdmin(object):
    list_display = ['title', "category", "tags", 'is_active', 'is_hot', 'is_recommend', 'is_banner', 'is_commentable', 'index', "front_image", "front_image_type", 'browse_password']
    list_editable = ['is_active', 'is_hot', 'is_recommend', 'is_banner', 'is_commentable', 'index']
    search_fields = ['title']
    exclude = ['post_type', 'browse_password_encrypt']

    class ArticleTagInline(object):
        model = PostTag
        extra = 1

    inlines = [ArticleTagInline, ArticleDetailAdmin]


xadmin.site.register(ArticleInfo, ArticleInfoAdmin)
