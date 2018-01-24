#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 上午11:37
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : search_indexes.py
# @Software: PyCharm


import datetime
from django.db.models import Q
from haystack import indexes
from .models import ArticleInfo, ArticleDetail


class ArticleInfoIndex(indexes.SearchIndex, indexes.Indexable):
    """
    文章基本信息索引
    """
    text = indexes.CharField(document=True, use_template=True)
    subtitle = indexes.CharField()
    abstract = indexes.CharField()
    desc = indexes.CharField()
    author = indexes.CharField()

    def get_model(self):
        return ArticleInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(add_time__lte=datetime.datetime.now(), is_active=True)


class ArticleDetailIndex(indexes.SearchIndex, indexes.Indexable):
    """
    文章详细信息索引
    """
    text = indexes.CharField(document=True, use_template=True)
    formatted_content = indexes.CharField(model_attr='formatted_content')

    def get_model(self):
        return ArticleDetail

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(article_info__is_active=True)