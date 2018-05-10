#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:13
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from .models import CommentInfo
from .serializers import CommentDetailInfoSerializer, CreateCommentSerializer, CommentLikeSerializer
from .filters import CommentFilter
from base.utils import CustomeLimitOffsetPagination


class CommentDetailListViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    List:
        评论列表页
    """
    queryset = CommentInfo.objects.all()
    # 分页设置
    pagination_class = CustomeLimitOffsetPagination
    
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CommentFilter
    ordering_fields = ('add_time',)
    ordering = ('-add_time',)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentDetailInfoSerializer
        elif self.action == "create":
            return CreateCommentSerializer
        return CommentDetailInfoSerializer


class CommentLikeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    文章点赞
    """
    serializer_class = CommentLikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        comment_id = serializer.validated_data["comment_id"]
        operation = serializer.validated_data["operation"]

        comment = CommentInfo.objects.filter(id=comment_id)[0]

        if comment is not None:
            if bool(operation):
                comment.like_num += 1
            else:
                comment.unlike_num += 1
            comment.save()
            context = {
                "comment": comment_id
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                "error": '未找到评论'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


