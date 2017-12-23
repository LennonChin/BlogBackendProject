#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from material.models import MaterialCategory, MaterialTag, PostBaseInfo, MaterialBanner, MaterialCamera, \
    MaterialPicture, MaterialSocial, MaterialMaster


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


class SingleLevelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTag
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCamera
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
    camera = CameraSerializer()

    class Meta:
        model = MaterialPicture
        fields = "__all__"


class MaterialPostBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBaseInfo
        fields = (
        'id', 'title', 'desc', 'like_num', 'comment_num', 'click_num', 'front_image', 'is_hot', 'is_recommend',
        'post_type', 'add_time')


class MaterialBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBanner
        fields = "__all__"


class MaterialSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialSocial
        fields = "__all__"


class MaterialMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialMaster
        fields = "__all__"
