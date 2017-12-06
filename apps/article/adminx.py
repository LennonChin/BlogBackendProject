#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin
from django import forms
from .models import ArticleInfo, ArticleDetail, ArticleTag
from pagedown.widgets import AdminPagedownWidget


class ArticleInfoAdmin(object):
    list_display = ['title', 'subtitle', "abstract", "desc", "author", "category", "tags", "detail", "front_image",
                    "front_image_type"]
    search_fields = ['title', ]

    class ArticleTagInline(object):
        model = ArticleTag
        style = "tab"
        extra = 1

    inlines = [ArticleTagInline]


class ArticleDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = ArticleDetail
        fields = '__all__'


class ArticleDetailAdmin(object):
    # form = ArticleDetailForm
    list_display = ['origin_content', 'formatted_content', "add_time"]
    search_fields = ['origin_content', ]


class ArticleTagAdmin(object):
    list_display = ['article', 'tag', "add_time"]
    search_fields = ['article', ]


xadmin.site.register(ArticleInfo, ArticleInfoAdmin)
xadmin.site.register(ArticleDetail, ArticleDetailAdmin)
xadmin.site.register(ArticleTag, ArticleTagAdmin)
