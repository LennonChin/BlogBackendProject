#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 上午11:08
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from .serializers import QiniuTokenSerializer
from user_operation.models import QiniuTokenRecord
from base.utils import generate_qiniu_token, generate_qiniu_random_filename


class QiniuTokenViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    获取QiniuToken
    """
    serializer_class = QiniuTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # status 400

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
        error = ''
        try:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            elif 'REMOTE_ADDR' in request.META:
                ip = request.META['REMOTE_ADDR']
        except Exception as e:
            error = e

        # 生成Token返回
        object_name = generate_qiniu_random_filename(64)
        object_name, token, base_url, expire_time = generate_qiniu_token(object_name, use_type)
        token_record = QiniuTokenRecord(ip=ip, token=token, use_type=use_type)
        token_record.save()
        context = {
            'key': object_name,
            'token': token,
            'base_url': base_url,
            'expire': expire_time,
            'error': error
        }
        return Response(context, status.HTTP_201_CREATED)
