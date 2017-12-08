#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

from .models import AlbumInfo, AlbumPhoto, AlbumTag


class AlbumInfoAdmin(object):
    list_display = ['title', 'subtitle', "abstract", "desc", "author", "category", "tags", "pictures", "front_image",
                    "front_image_type"]
    search_fields = ['title', 'subtitle', "abstract", "desc", "category"]

    class AlbumTagInline(object):
        model = AlbumTag
        style = "tab"
        extra = 1

    class AlbumPhotoInline(object):
        model = AlbumPhoto
        style = "tab"
        extra = 1

    inlines = [AlbumTagInline, AlbumPhotoInline]


class AlbumPhotoAdmin(object):
    list_display = ['album', "picture", "add_time"]
    search_fields = ['album', 'picture']


class AlbumTagAdmin(object):
    list_display = ['album', 'tag', "add_time"]
    search_fields = ['album', 'tag']


xadmin.site.register(AlbumInfo, AlbumInfoAdmin)
xadmin.site.register(AlbumPhoto, AlbumPhotoAdmin)
xadmin.site.register(AlbumTag, AlbumTagAdmin)
