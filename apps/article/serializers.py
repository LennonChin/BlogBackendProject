# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from article.models import ArticleInfo
from material.serializers import SingleLevelCategorySerializer, TagSerializer


class ArticleDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = ArticleInfo
        exclude = ('origin_content', )


class ArticleBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = ArticleInfo
        exclude = ('subtitle', 'abstract', 'origin_content', 'formatted_content')
