#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import ArticleInfo


class ArticleInfodAdmin(object):
    list_display = ['title', 'subtitle', "abstract", "desc", "author", "category", "tags", "detail", "front_image", "front_image_type"]


xadmin.site.register(ArticleInfo, ArticleInfodAdmin)