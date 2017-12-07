#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from material.models import MaterialCategory, MaterialTag


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_category = CategorySerializer3(many=True)

    class Meta:
        model = MaterialCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_category = CategorySerializer2(many=True)

    class Meta:
        model = MaterialCategory
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialTag
        fields = "__all__"