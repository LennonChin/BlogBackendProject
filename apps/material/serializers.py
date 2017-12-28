#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from datetime import datetime
from rest_framework import serializers
from material.models import MaterialCategory, MaterialTag, MaterialLicense, PostBaseInfo, MaterialBanner, \
    MaterialCamera, \
    MaterialPicture, MaterialCommentInfo, MaterialCommentDetail, MaterialSocial, MaterialMaster
from user.serializers import GuestSerializer


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


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialLicense
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


class CommentDetailSerializer(serializers.ModelSerializer):
    origin_content = serializers.CharField(write_only=True, label='原始内容')
    formatted_content = serializers.CharField(read_only=True)

    class Meta:
        model = MaterialCommentDetail
        fields = ('origin_content', 'formatted_content', 'update_time')


class CommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        comment_info = MaterialCommentInfo.objects.create(**validated_data)
        # 处理评论详情
        instance = MaterialCommentDetail.objects.create(comment_info=comment_info, **detail_data)
        return comment_info

    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


class CommentBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


class MaterialPostBaseInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = PostBaseInfo
        fields = (
            'id', 'title', 'desc', 'tags', 'like_num', 'comment_num', 'click_num', 'front_image', 'front_image_type',
            'is_hot',
            'is_recommend', 'is_banner',
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
