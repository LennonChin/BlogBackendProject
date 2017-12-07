#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:13
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, generics, viewsets, filters
from rest_framework.response import Response

from .models import MaterialCategory
from .serializers import CategorySerializer
from .filters import CategoryFilter


class CategoryListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        分类列表页
    """
    queryset = MaterialCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'code', 'desc')
    ordering_fields = ('category_type', 'is_tab')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

