#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:52
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

from django.db.models import Q
import django_filters
from .models import ArticleInfo


class ArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """
    time_min = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    time_max = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 查找指定分类下的所有文章
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = ArticleInfo
        fields = ['time_min', 'time_max', 'is_hot', 'is_recommend', 'is_banner']
