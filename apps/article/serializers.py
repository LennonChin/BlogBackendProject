# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from article.models import ArticleInfo, ArticleDetail
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


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleDetail
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    detail = ArticleDetailSerializer()
    # tags = TagSerializer(read_only=True)

    class Meta:
        model = ArticleInfo
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return ArticleInfo.objects.create(**validated_data)