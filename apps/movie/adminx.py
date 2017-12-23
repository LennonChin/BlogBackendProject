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

from .models import MovieInfo, MovieDetail
from material.models import PostTag
from pagedown.widgets import AdminPagedownWidget


class MovieDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = MovieDetail
        fields = '__all__'


class MovieDetailAdmin(object):
    form = MovieDetailForm
    exclude = ['formatted_content']
    model = MovieDetail

    def save_models(self):
        # 转换Markdown为格式化的HTML
        self.new_obj.formatted_content = markdown.markdown(self.new_obj.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc',
                                                           ])
        self.new_obj.save()


class MovieInfoAdmin(object):
    list_display = ['title', "front_image", "front_image_type"]
    search_fields = ['title']
    exclude = ['post_type']

    class ArticleTagInline(object):
        model = PostTag
        extra = 1

    inlines = [ArticleTagInline, MovieDetailAdmin]

    def save_models(self):
        # 手动设置类型
        self.new_obj.post_type = "movie"
        self.new_obj.save()


xadmin.site.register(MovieInfo, MovieInfoAdmin)
