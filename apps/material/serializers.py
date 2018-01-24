#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from material.models import MaterialCategory, MaterialTag, MaterialLicense, PostBaseInfo, MaterialBanner, \
    MaterialCamera, \
    MaterialPicture, MaterialCommentInfo, MaterialCommentDetail, MaterialSocial, MaterialMaster
from user.serializers import GuestSerializer

# 搜索
from drf_haystack.serializers import HaystackSerializer, HighlighterMixin
from .search_indexes import PostBaseInfoIndex


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
    update_time = serializers.DateTimeField(required=False)

    class Meta:
        model = MaterialCommentDetail
        fields = ('origin_content', 'formatted_content', 'update_time')


# 子级评论排序
class OrderSubCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('add_time')[:10]
        return super(OrderSubCommentListSerializer, self).to_representation(data)


# 子级评论
class SubCommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()

    class Meta:
        list_serializer_class = OrderSubCommentListSerializer
        model = MaterialCommentInfo
        fields = "__all__"


# 评论详细信息
class CommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()
    sub_comment = SubCommentDetailInfoSerializer(many=True)

    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


# 评论基本信息
class CommentBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


# 创建评论使用的serializer
class CreateCommentSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        # 创建评论
        comment_info = MaterialCommentInfo.objects.create(**validated_data)
        # 处理评论详情
        MaterialCommentDetail.objects.create(comment_info=comment_info, **detail_data)
        # 修改根级评论数数据
        if comment_info.parent_comment_id:
            parent_comment = MaterialCommentInfo.objects.get(id=comment_info.parent_comment_id)
            parent_comment.comment_num += 1
            parent_comment.save()
        # 文章的评论数数据
        post = comment_info.post
        post.comment_num += 1
        post.save()
        return comment_info

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
            'post_type', 'browse_password_encrypt', 'add_time')


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


# 搜索相关
class PostBaseInfoSearchSerializer(HaystackSerializer, HighlighterMixin):

    highlighter_css_class = "keyword"
    highlighter_html_tag = "em"

    class Meta:
        index_classes = [PostBaseInfoIndex, ]
        fields = ['title', 'subtitle', 'abstract', 'desc', 'author']
