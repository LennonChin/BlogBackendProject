# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:52'

from rest_framework import mixins, generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import ArticleInfo
from .serializers import ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 12
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
    pagination_class = ArticlePagination

    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)