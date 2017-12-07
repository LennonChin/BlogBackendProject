#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午3:31
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

import django_filters
from .models import MaterialCategory


class CategoryFilter(django_filters.rest_framework.FilterSet):
    """
    分类的过滤类
    """
    level_min = django_filters.NumberFilter(name='category_type', lookup_expr='gte')
    level_max = django_filters.NumberFilter(name='category_type', lookup_expr='lte')

    class Meta:
        model = MaterialCategory
        fields = ['level_min', 'level_max', 'is_tab']