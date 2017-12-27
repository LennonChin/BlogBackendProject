# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from article.models import ArticleInfo, ArticleDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleDetail
        fields = ('formatted_content',)


class ArticleBaseInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = ArticleInfo
        fields = (
            'id', 'title', 'desc', 'author', 'tags', 'click_num', 'like_num', 'comment_num', 'post_type',
            'front_image', 'is_recommend', 'is_hot', 'is_banner',
            'front_image_type', 'add_time')


class ArticleDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    detail = ArticleDetailSerializer()

    class Meta:
        model = ArticleInfo
        fields = "__all__"
