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
from .models import MaterialCategory, MaterialTag, MaterialPicture, MaterialBanner, PostBaseInfo, MaterialSocial, \
    MaterialMaster


class MaterialCategoryAdmin(object):
    list_display = ['name', 'code', "desc", "category_type", "parent_category", "is_tab", "add_time"]
    list_editable = ["is_tab", ]
    search_fields = ['name', ]


class MaterialTagAdmin(object):
    list_display = ['name', 'subname', "category"]
    search_fields = ['name', ]


class MaterialPictureAdmin(object):
    list_display = ['title', 'subtitle', 'abstract', "desc", "image", "link"]
    search_fields = ['title', 'subtitle', 'abstract', "desc", "link"]


class MaterialBannerAdmin(object):
    list_display = ['title', 'image', "url", "index", "add_time"]
    search_fields = ['title', 'url']


class MaterialPostInfoAdmin(object):
    list_display = ['title', 'subtitle']
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
xadmin.site.register(MaterialBanner, MaterialBannerAdmin)
xadmin.site.register(PostBaseInfo, MaterialPostInfoAdmin)
xadmin.site.register(MaterialSocial, MaterialSocialAdmin)
xadmin.site.register(MaterialMaster, MaterialMasterAdmin)
