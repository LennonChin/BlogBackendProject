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
    list_display = ('title', 'category', 'is_active', 'is_hot', 'is_recommend', 'is_banner', 'is_commentable', "tags", 'pictures', 'front_image', 'front_image_type')
    list_editable = ['is_active', 'is_hot', 'is_recommend', 'is_banner', 'is_commentable']
    search_fields = ('title', 'subtitle', 'abstract', 'desc', 'category')
    exclude = ('post_type', 'browse_password_encrypt')

    class AlbumTagInline(object):
        model = PostTag
        style = 'tab'
        extra = 1

    class AlbumPhotoInline(object):
        model = AlbumPhoto
        extra = 1

    inlines = (AlbumTagInline, AlbumPhotoInline)


class AlbumPhotoAdmin(object):
    list_display = ('album', 'picture', 'add_time')
    search_fields = ('album', 'picture')


xadmin.site.register(AlbumInfo, AlbumInfoAdmin)
xadmin.site.register(AlbumPhoto, AlbumPhotoAdmin)
