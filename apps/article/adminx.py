#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

import markdown
from django import forms

from .models import ArticleInfo
from material.models import PostTag
from pagedown.widgets import AdminPagedownWidget


class ArticleDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = ArticleInfo
        fields = '__all__'


class ArticleInfoAdmin(object):
    form = ArticleDetailForm
    list_display = ['title', "category", "tags", "front_image",
                    "front_image_type"]
    search_fields = ['title', 'origin_content']
    exclude = ['formatted_content', 'post_type']

    def save_models(self):
        # 转换Markdown为格式化的HTML
        self.new_obj.formatted_content = markdown.markdown(self.new_obj.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc'
                                                           ])
        self.new_obj.save()

    class ArticleTagInline(object):
        model = PostTag
        extra = 1

    inlines = [ArticleTagInline]


xadmin.site.register(ArticleInfo, ArticleInfoAdmin)
