#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午3:31
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

from django.db.models import Q
import django_filters
from .models import SiteInfo


class SiteInfoFilter(django_filters.rest_framework.FilterSet):
    """
    网站信息过滤类
    """

    class Meta:
        model = SiteInfo
        fields = ['is_live']


