# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:52'

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response

from .models import AlbumInfo
from .serializers import AlbumBaseInfoSerializer, AlbumDetailInfoSerializer
from .filters import AlbumFilter
from base.utils import CustomeLimitOffsetPagination


class AlbumBaseInfoListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        图集列表页
    """
    queryset = AlbumInfo.objects.filter(is_active=True)
    serializer_class = AlbumBaseInfoSerializer

    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AlbumFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('click_num', 'like_num', 'comment_num', 'add_time')
    exclude = ('post_type', )

    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AlbumDetailInfoListViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        图集列表页
    """
    queryset = AlbumInfo.objects.filter(is_active=True)
    serializer_class = AlbumDetailInfoSerializer

    # 过滤，搜索，排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AlbumFilter
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