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
from .models import MaterialCategory, MaterialTag, Banner


class MaterialCategoryAdmin(object):
    list_display = ['name', 'code', "desc", "category_type", "parent_category", "is_tab", "add_time"]
    list_editable = ["is_tab", ]
    search_fields = ['name', ]


class MaterialTagAdmin(object):
    list_display = ['name', 'subname', "category"]
    search_fields = ['name', ]


class MaterialBannerAdmin(object):
    list_display = ['title', 'image', "url", "index", "add_time"]
    search_fields = ['title', 'url']

xadmin.site.register(MaterialCategory, MaterialCategoryAdmin)
xadmin.site.register(MaterialTag, MaterialTagAdmin)
xadmin.site.register(Banner, MaterialBannerAdmin)
