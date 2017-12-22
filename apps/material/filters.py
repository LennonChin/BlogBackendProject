#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午3:31
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

from django.db.models import Q
import django_filters
from .models import MaterialCategory, MaterialBanner


class CategoryFilter(django_filters.rest_framework.FilterSet):
    """
    分类的过滤类
    """
    level_min = django_filters.NumberFilter(name='category_type', lookup_expr='gte')
    level_max = django_filters.NumberFilter(name='category_type', lookup_expr='lte')

    class Meta:
        model = MaterialCategory
        fields = ['id', 'level_min', 'level_max', 'is_tab']


class MaterialBannerFilter(django_filters.rest_framework.FilterSet):
    """
    分类的过滤类
    """
    level_min = django_filters.NumberFilter(name='category_type', lookup_expr='gte')
    level_max = django_filters.NumberFilter(name='category_type', lookup_expr='lte')

    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 查找指定分类下的banner
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = MaterialBanner
        fields = ['title', 'url', 'index']