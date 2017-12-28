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
    class Meta:
        model = GuestProfile
        fields = "__all__"


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=11)

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("手机号码格式错误")

        # 验证发送频率
        ten_minutes_ago = datetime.now() - timedelta(hours=0, minutes=10, seconds=0)
        if EmailVerifyRecord.objects.filter(add_time__gt=ten_minutes_ago, email=email):
            raise serializers.ValidationError("距离上一次发送未超过60秒")

        return email
