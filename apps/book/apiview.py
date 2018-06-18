# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:52'

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response

from .models import BookInfo, BookNoteInfo
from .serializers import BookBaseInfoSerializer, BookDetailInfoSerializer, BookNoteBaseInfoSerializer, BookNoteDetialInfoSerializer
from .filters import BookFilter, BookNoteFilter

from base.utils import CustomeLimitOffsetPagination


class BookBaseInfoListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        图书基本信息文章列表页
    """
    queryset = BookInfo.objects.filter(is_active=True)
    serializer_class = BookBaseInfoSerializer

    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BookFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num', 'index', 'add_time')
    ordering = ('-index', '-add_time')

    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BookDetailInfoListViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        图书详细信息列表页
    """
    queryset = BookInfo.objects.filter(is_active=True)
    serializer_class = BookDetailInfoSerializer

    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BookFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num')

    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.browse_password_encrypt:
            browse_auth = ""
            if 'browse_auth' in request.query_params:
                browse_auth = request.query_params['browse_auth']
            if browse_auth != instance.browse_password_encrypt:
                context = {
                    "error": "文章密码错误"
                }
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 图书笔记
class BookNoteBaseInfoListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        图书笔记信息列表页
    """
    queryset = BookNoteInfo.objects.filter(is_active=True)
    serializer_class = BookNoteBaseInfoSerializer

    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BookNoteFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num', 'index', 'add_time')
    ordering = ('-index', '-add_time')

    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BookNoteDetailInfoListViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        图书笔记信息列表页
    """
    queryset = BookNoteInfo.objects.filter(is_active=True)
    serializer_class = BookNoteDetialInfoSerializer

    # 过滤，搜索，排序
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_class = BookFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num')

    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.browse_password_encrypt:
            browse_auth = ""
            if 'browse_auth' in request.query_params:
                browse_auth = request.query_params['browse_auth']
            if browse_auth != instance.browse_password_encrypt:
                context = {
                    "error": "文章密码错误"
                }
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)