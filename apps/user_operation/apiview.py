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
from .serializers import PostLikeSerializer, CommentLikeSerializer, QiniuTokenSerializer
from material.models import PostBaseInfo, MaterialCommentInfo
from user_operation.models import QiniuTokenRecord
from base.utils import generate_qiniu_token, generate_qiniu_random_filename


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

        comment = MaterialCommentInfo.objects.filter(id=comment_id)[0]

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


class QiniuTokenViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    获取QiniuToken
    """
    serializer_class = QiniuTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        suffix = serializer.validated_data['suffix']
        use_type = serializer.validated_data['use_type']

        if use_type is None:
            # 类型未填写
            context = {
                'error': '请指定操作类型'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if suffix is None:
            # 后缀名未提供
            context = {
                'error': '请指定上传文件的类型'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        ip = '0.0.0.0'
        print(request.META)
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'REMOTE_ADDR' in request.META:
            ip = request.META['REMOTE_ADDR']

        # ten_second_age = datetime.now() - timedelta(hours=0, minutes=0, seconds=10)
        # token_records = QiniuTokenRecord.objects.filter(ip=ip)
        # if len(token_records):
        #     token_record = token_records[0]
        #     if token_record.add_time < ten_second_age:
        #         # 验证码过期
        #         context = {
        #             "error": '请求太频繁'
        #         }
        #         return Response(context, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # 生成Token返回
        object_name = generate_qiniu_random_filename(64)
        object_name, token, base_url, expire_time = generate_qiniu_token(object_name, use_type)
        token_record = QiniuTokenRecord(ip=ip, token=token, use_type=use_type)
        token_record.save()
        context = {
            'key': object_name,
            'token': token,
            'base_url': base_url,
            'expire': expire_time
        }
        return Response(context, status.HTTP_201_CREATED)