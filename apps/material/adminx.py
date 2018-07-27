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
from .models import MaterialCategory, MaterialTag, MaterialLicense, MaterialPicture, MaterialBanner, PostBaseInfo, MaterialSocial, \
    MaterialMaster


class MaterialCategoryAdmin(object):
    list_display = ['name', 'desc', 'category_type', 'category_level', 'parent_category', 'is_active', "is_tab", 'index', 'add_time']
    list_editable = ['is_active', 'is_tab', 'index']
    search_fields = ['name', ]


class MaterialTagAdmin(object):
    list_display = ['name', 'en_name', 'color', 'category']
    search_fields = ['name', ]


class MaterialPictureAdmin(object):
    list_display = ['title', "desc", "image", "link"]
    search_fields = ['title', "desc", "link"]


class MaterialLicenseAdmin(object):
    list_display = ['name', 'desc', 'link']
    search_fields = ['name', 'desc', 'link']


class MaterialBannerAdmin(object):
    list_display = ['title', 'image', "url", "index", "add_time"]
    search_fields = ['title', 'url']


class MaterialPostInfoAdmin(object):
    list_display = ['title', 'is_hot', 'is_recommend', 'is_banner', 'is_commentable', "front_image", "front_image_type", 'browse_password', 'add_time']
    list_editable = ['is_hot', 'is_recommend', 'is_banner', 'is_commentable']
    search_fields = ['title', 'subtitle']


class MaterialSocialAdmin(object):
    list_display = ['name', 'desc', "image", "url"]
    search_fields = ['name', 'desc']


class MaterialMasterAdmin(object):
    list_display = ['name', 'desc', "image", "url", 'experience']
    search_fields = ['name', 'desc']


xadmin.site.register(MaterialCategory, MaterialCategoryAdmin)
xadmin.site.register(MaterialTag, MaterialTagAdmin)
xadmin.site.register(MaterialPicture, MaterialPictureAdmin)
xadmin.site.register(MaterialLicense, MaterialLicenseAdmin)
xadmin.site.register(MaterialBanner, MaterialBannerAdmin)
xadmin.site.register(PostBaseInfo, MaterialPostInfoAdmin)
xadmin.site.register(MaterialSocial, MaterialSocialAdmin)
xadmin.site.register(MaterialMaster, MaterialMasterAdmin)
