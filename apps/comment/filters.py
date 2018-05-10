#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午3:31
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : filters.py
# @Software: PyCharm

import django_filters
from .models import CommentInfo


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    评论的过滤类
    """
    time_min = django_filters.DateFilter(name='add_time', lookup_expr='gte')
    time_max = django_filters.DateFilter(name='add_time', lookup_expr='lte')

    post_id = django_filters.NumberFilter(method='post_id_filter')

    # 查找指定文章下的评论
    def post_id_filter(self, queryset, name, value):
        return queryset.filter(post_id=value)

    class Meta:
        model = CommentInfo
        fields = ['time_min', 'time_max', 'is_hot', 'is_recommend', 'is_active', 'comment_level', 'parent_comment',
                  'reply_to_comment']
