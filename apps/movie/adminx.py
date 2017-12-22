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

from .models import MovieInfo
from pagedown.widgets import AdminPagedownWidget


class MovieDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = MovieInfo
        fields = '__all__'


class MovieDetailAdmin(object):
    form = MovieDetailForm
    list_display = ['title', "category", "tags", "front_image", "front_image_type"]
    search_fields = ['title', 'origin_content']
    exclude = ['formatted_content', 'post_type']

    def save_models(self):
        # 手动设置类型
        self.new_obj.post_type = "movie"
        # 转换Markdown为格式化的HTML
        self.new_obj.formatted_content = markdown.markdown(self.new_obj.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc',
                                                           ])
        self.new_obj.save()


class MovieTagAdmin(object):
    list_display = ['movie', 'tag', "add_time"]
    search_fields = ['movie', 'tag']


xadmin.site.register(MovieInfo, MovieDetailAdmin)
