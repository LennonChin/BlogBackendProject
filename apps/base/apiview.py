# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from rest_framework import mixins, viewsets

from .models import BloggerInfo, FriendLink
from .serializers import BloggerInfoSerializer, FriendLinksSerializer


class BloggerInfoViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        Banner列表页
    """
    queryset = BloggerInfo.objects.all()
    serializer_class = BloggerInfoSerializer


class FriendLinkListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        Banner列表页
    """
    queryset = FriendLink.objects.all()
    serializer_class = FriendLinksSerializer