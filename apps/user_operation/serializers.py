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
