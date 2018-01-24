#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 上午11:37
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : search_indexes.py
# @Software: PyCharm


import datetime
from haystack import indexes
from .models import PostBaseInfo


class PostBaseInfoIndex(indexes.SearchIndex, indexes.Indexable):
    """
    文章基本信息索引
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()
    subtitle = indexes.CharField()
    abstract = indexes.CharField()
    desc = indexes.CharField()
    author = indexes.CharField()

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.title, obj.subtitle, obj.abstract, obj.desc, obj.author
        ))

    def get_model(self):
        return PostBaseInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(add_time__lte=datetime.datetime.now(), is_active=True)