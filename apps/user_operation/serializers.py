#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

import re
from rest_framework import serializers


class PostLikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True, label='文章')


class QiniuTokenSerializer(serializers.Serializer):
    use_type = serializers.CharField(default='comment', required=False, label='操作类型')

    def validate_use_type(self, use_type):
        """
        验证操作类型
        :param use_type: 
        :return: 
        """
        CHOICES = ['comment']

        # 判断类型
        if use_type not in CHOICES:
            raise serializers.ValidationError("操作类型未提供")
        else:
            return use_type
