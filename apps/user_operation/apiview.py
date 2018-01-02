#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 上午11:08
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from datetime import datetime, timedelta
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from .serializers import PostLikeSerializer
from material.models import PostBaseInfo


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