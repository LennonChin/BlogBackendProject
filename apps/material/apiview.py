#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:13
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from rest_framework import mixins, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .models import MaterialCategory, MaterialTag, MaterialBanner, PostBaseInfo
from .serializers import CategorySerializer, SingleLevelCategorySerializer, TagSerializer, MaterialBannerSerializer, MaterialPostBaseInfoSerializer, PostLikeSerializer
from .filters import CategoryFilter, MaterialBannerFilter, PostBaseInfoFilter
from base.utils import CustomeLimitOffsetPagination, CustomePageNumberPagination


class CategoryListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        分类列表页
    """
    queryset = MaterialCategory.objects.filter(is_active=True)
    # 分页设置
    pagination_class = CustomePageNumberPagination
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'category_type', 'desc')
    ordering_fields = ('category_level', 'index')
    ordering = ('index',)


class SingleLevelCategoryListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        单级分类列表页
    """
    queryset = MaterialCategory.objects.filter(is_active=True)
    # 分页设置
    pagination_class = CustomePageNumberPagination
    serializer_class = SingleLevelCategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'category_type', 'desc')
    ordering_fields = ('category_level', 'index')
    ordering = ('index',)


class TagListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        标签列表页
    """
    queryset = MaterialTag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name', 'subname')
    ordering_fields = ('name', 'subname')


class MaterialBannerListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        Banner列表页
    """
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = MaterialBannerFilter
    queryset = MaterialBanner.objects.all().order_by("-index")
    serializer_class = MaterialBannerSerializer


class PostBaseInfoListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        时间轴列表页
    """
    queryset = PostBaseInfo.objects.all()
    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PostBaseInfoFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('id', 'click_num', 'like_num', 'comment_num', 'add_time')
    serializer_class = MaterialPostBaseInfoSerializer



class PostLikeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    文章点赞
    """
    serializer_class = PostLikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        post_id = serializer.validated_data["post_id"]

        post = PostBaseInfo.objects.filter(id=post_id)[0]

        if post is not None:
            post.like_num += 1
            post.save()
            context = {
                "post": post_id
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                "error": '未找到文章'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)