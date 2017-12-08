#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

from .models import SiteInfo, BloggerInfo, BloggerSocial, BloggerMaster


class SiteInfoAdmin(object):
    list_display = ['name', 'name_en', "desc", "copyright", "icp"]
    search_fields = ['name', 'name_en', 'is_live']


class BloggerInfoAdmin(object):
    list_display = ['name', 'name_en', 'desc', 'avatar', 'socials', 'masters']
    search_fields = ['name', 'name_en', 'desc']

    class BloggerSocialInline(object):
        model = BloggerSocial
        style = "tab"
        extra = 1

    class BloggerMasterInline(object):
        model = BloggerMaster
        style = "tab"
        extra = 1

    inlines = [BloggerSocialInline, BloggerMasterInline]


xadmin.site.register(SiteInfo, SiteInfoAdmin)
xadmin.site.register(BloggerInfo, BloggerInfoAdmin)
