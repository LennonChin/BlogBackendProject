# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from article.models import ArticleInfo, ArticleDetail
from material.serializers import CategorySerializer, TagSerializer


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleDetail
        fields = ["formatted_content", ]


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    detail = ArticleDetailSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = ArticleInfo
        fields = "__all__"
