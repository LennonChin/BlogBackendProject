#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:52
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

import django_filters
from .models import ArticleInfo


class ArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """
    time_min = django_filters.NumberFilter(name='add_time', lookup_expr='gte')
    time_max = django_filters.NumberFilter(name='add_time', lookup_expr='lte')

    class Meta:
        model = ArticleInfo
        fields = ['time_min', 'time_max', 'is_hot', 'is_recommend']