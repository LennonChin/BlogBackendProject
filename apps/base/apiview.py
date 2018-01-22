# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import SiteInfo, BloggerInfo, FriendLink
from .serializers import BloggerInfoSerializer, SiteInfoSerializer, FriendLinkSerializer
from .filters import SiteInfoFilter


class SiteInfoViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        网站信息
    """
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = SiteInfoFilter


class BloggerInfoViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        博主信息
    """
    queryset = BloggerInfo.objects.all()
    serializer_class = BloggerInfoSerializer


class FriendLinkListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        友情链接列表页
    """
    queryset = FriendLink.objects.all()
    serializer_class = FriendLinkSerializer
