#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from .models import GuestProfile, EmailVerifyRecord
from base.const import REGEX_EMAIL


class GuestSerializer(serializers.ModelSerializer):
    is_blogger = serializers.SerializerMethodField()

    def get_is_blogger(self, guest):
        if guest.email:
            return guest.email == '243316474@qq.com'
        else:
            return False

    class Meta:
        model = GuestProfile
        fields = ('id', 'nick_name', 'avatar', 'is_blogger')


class EmailSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50, min_length=1, required=True, label='昵称')
    email = serializers.EmailField(required=True, label='邮箱')

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式错误")

        # 验证发送频率
        ten_minutes_ago = datetime.now() - timedelta(hours=0, minutes=0, seconds=30)
        if EmailVerifyRecord.objects.filter(send_time__gt=ten_minutes_ago, email=email):
            raise serializers.ValidationError("请求发送过于频繁，请间隔30秒后重试")

        return email


class EmailVerifySerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50, min_length=1, required=True, label='昵称')
    email = serializers.EmailField(required=True, label='邮箱')
    code = serializers.CharField(max_length=4, min_length=4, required=False, label='验证码')

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式错误")

        return email
