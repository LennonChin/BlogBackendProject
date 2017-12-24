#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin
from xadmin import views
from .models import SiteInfo, BloggerInfo, BloggerSocial, BloggerMaster, FriendLink


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Diomedes"
    site_footer = "Diomedes"


class SiteInfoAdmin(object):
    list_display = ['name', 'name_en', "desc", "copyright", "icp"]
    search_fields = ['name', 'name_en', 'is_live']


class BloggerInfoAdmin(object):
    list_display = ['name', 'name_en', 'desc', 'avatar', 'socials', 'masters']
    search_fields = ['name', 'name_en', 'desc']

    class BloggerSocialInline(object):
        model = BloggerSocial
        extra = 1

    class BloggerMasterInline(object):
        model = BloggerMaster
        extra = 1

    inlines = [BloggerSocialInline, BloggerMasterInline]


class FriendLinkAdmin(object):
    list_display = ['name', 'desc', 'url']
    search_fields = ['name', 'desc', 'url']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(SiteInfo, SiteInfoAdmin)
xadmin.site.register(BloggerInfo, BloggerInfoAdmin)
xadmin.site.register(FriendLink, FriendLinkAdmin)
