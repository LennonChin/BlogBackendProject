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

from .models import MovieInfo, MovieDetail, MovieTag
from pagedown.widgets import AdminPagedownWidget


class MovieInfoAdmin(object):
    list_display = ['title', "desc", "directors", "actors", 'category', 'region', 'language', "length", "detail",
                    "front_image", "front_image_type"]
    search_fields = ['title', "desc", "directors", "actors", 'category', 'region', 'language']

    class MovieTagInline(object):
        model = MovieTag
        style = "tab"
        extra = 1

    inlines = [MovieTagInline]


class MovieDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = MovieDetail
        fields = '__all__'


class MovieDetailAdmin(object):
    form = MovieDetailForm
    list_display = ['origin_content', "add_time"]
    exclude = ['formatted_content', ]
    search_fields = ['origin_content', ]

    def save_models(self):
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


xadmin.site.register(MovieInfo, MovieInfoAdmin)
xadmin.site.register(MovieDetail, MovieDetailAdmin)
xadmin.site.register(MovieTag, MovieTagAdmin)
