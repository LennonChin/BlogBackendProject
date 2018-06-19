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
from .serializers import CategorySerializer, SingleLevelCategorySerializer, TagSerializer, MaterialBannerSerializer, MaterialPostBaseInfoSerializer, PostLikeSerializer, VerifyPostAuthSerializer
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
    queryset = PostBaseInfo.objects.filter(is_active=True)
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


class VerifyPostAuthViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    验证文章权限
    """
    serializer_class = VerifyPostAuthSerializer

    def create(self, request, *args, **kwargs):
        """
        验证文章权限
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 验证结果
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        post_id = serializer.validated_data['post_id']
        browse_auth = serializer.validated_data['browse_auth']

        if post_id is None:
            # 文章为空
            context = {
                "error": '请指定文章'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if browse_auth is None:
            # 阅读密码为空
            context = {
                "error": '请提供阅读密码'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        posts = PostBaseInfo.objects.filter(id=post_id)

        if len(posts):
            if posts[0].browse_password_encrypt == browse_auth:
                context = {
                    'post_id': posts[0].id
                }
                return Response(context, status.HTTP_202_ACCEPTED)
            else:
                # 阅读密码错误
                context = {
                    'error': '阅读密码错误'
                }
                return Response(context, status=status.HTTP_403_FORBIDDEN)
        else:
            # 无此文章
            context = {
                'error': '没有此文章，请重试',
                'post_id': post_id
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)