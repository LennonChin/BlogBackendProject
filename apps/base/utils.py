#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午5:41
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : utils.py
# @Software: PyCharm

from rest_framework.pagination import PageNumberPagination


# 分页
class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100
