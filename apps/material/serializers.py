#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from material.models import MaterialCategory, MaterialTag, MaterialLicense, PostBaseInfo, MaterialBanner, \
    MaterialCamera, MaterialPicture, MaterialSocial, MaterialMaster, PostTag

from BlogBackendProject.settings import MEDIA_URL_PREFIX


# 子级分类排序过滤，只取显示在tab上的，且按index排序
class OrderCategoryListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(is_active=True).order_by('index')
        return super(OrderCategoryListSerializer, self).to_representation(data)


class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = OrderCategoryListSerializer
        model = MaterialCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_category = CategorySerializer3(many=True)

    class Meta:
        list_serializer_class = OrderCategoryListSerializer
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
    related_post_num = serializers.SerializerMethodField()

    def get_related_post_num(self, tag):
        return len(PostTag.objects.filter(tag__id=tag.id))

    class Meta:
        model = MaterialTag
        fields = ('name', 'en_name', 'color', 'related_post_num')


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


class MaterialPostBaseInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, article):
        if article.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, article.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = PostBaseInfo
        fields = (
            'id', 'title', 'en_title', 'desc', 'en_desc', 'tags', 'like_num', 'comment_num', 'click_num', 'front_image', 'front_image_type',
            'is_hot',
            'is_recommend', 'is_banner', 'is_commentable',
            'post_type', 'need_auth', 'add_time')


class MaterialBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialBanner
        fields = "__all__"


class MaterialSocialSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, social):
        if social.image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, social.image)

    class Meta:
        model = MaterialSocial
        fields = ('id', 'name', 'image', 'url', 'desc')


class MaterialMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialMaster
        fields = "__all__"


class PostLikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True, label='文章')


class VerifyPostAuthSerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=11, min_length=1, required=True, label='文章')
    browse_auth = serializers.CharField(max_length=64, min_length=6, required=True, label='阅读密码')
