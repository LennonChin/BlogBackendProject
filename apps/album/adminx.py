#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

from .models import AlbumInfo, AlbumPhoto
from material.models import PostTag


class AlbumInfoAdmin(object):
    list_display = ['title', "category", "tags", "pictures", "front_image", "front_image_type"]
    search_fields = ['title', 'subtitle', "abstract", "desc", "category"]
    exclude = ['post_type', ]

    def save_models(self):
        # 手动设置类型
        self.new_obj.post_type = "album"
        self.new_obj.save()

    class AlbumTagInline(object):
        model = PostTag
        style = "tab"
        extra = 1

    class AlbumPhotoInline(object):
        model = AlbumPhoto
        extra = 1

    inlines = [AlbumTagInline, AlbumPhotoInline]


class AlbumPhotoAdmin(object):
    list_display = ['album', "picture", "add_time"]
    search_fields = ['album', 'picture']


xadmin.site.register(AlbumInfo, AlbumInfoAdmin)
xadmin.site.register(AlbumPhoto, AlbumPhotoAdmin)
