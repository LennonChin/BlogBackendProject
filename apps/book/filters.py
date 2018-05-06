#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:52
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

from django.db.models import Q
import django_filters
from .models import BookInfo, BookNoteInfo


class BookFilter(django_filters.rest_framework.FilterSet):
    """
    书籍的过滤类
    """
    time_min = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    time_max = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 查找指定分类下的所有图书`
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = BookInfo
        fields = ['time_min', 'time_max', 'is_hot', 'is_recommend']


class BookNoteFilter(django_filters.rest_framework.FilterSet):
    """
    书籍笔记的过滤类
    """
    time_min = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    time_max = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 查找指定分类下的所有图书`
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = BookNoteInfo
        fields = ['time_min', 'time_max', 'is_hot', 'is_recommend']
