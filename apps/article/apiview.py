# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:52'

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import ArticleInfo
from .serializers import ArticleSerializer
from .filters import ArticleFilter


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class ArticleListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        商品列表页
    """
    queryset = ArticleInfo.objects.all()
    serializer_class = ArticleSerializer
    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ArticleFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num')

    # 分页设置
    pagination_class = ArticlePagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)