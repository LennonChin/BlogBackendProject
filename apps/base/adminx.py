#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin
from xadmin import views
from .models import SiteInfo, NavigationLink, BloggerInfo, BloggerSocial, BloggerMaster, FriendLink, SiteInfoNavigation


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Diomedes"
    site_footer = "Diomedes"


class SiteInfoAdmin(object):
    list_display = ['name', 'is_live', 'is_force_refresh', "desc", "copyright", "icp", 'access_password']
    list_editable = ["is_force_refresh", '']
    search_fields = ['name', 'name_en']
    exclude = ['browse_password_encrypt']

    class NavigationLinkInline(object):
        model = SiteInfoNavigation
        extra = 1

    inlines = [NavigationLinkInline]


class NavigationLinkAdmin(object):
    list_display = ['name', 'url']
    search_fields = ['name', 'url']


class BloggerInfoAdmin(object):
    list_display = ['name', 'desc', 'avatar', 'socials', 'masters']
    search_fields = ['name', 'desc']

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
xadmin.site.register(NavigationLink, NavigationLinkAdmin)
xadmin.site.register(FriendLink, FriendLinkAdmin)
