# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from movie.models import MovieInfo
from material.serializers import SingleLevelCategorySerializer, TagSerializer


class MovieDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = MovieInfo
        exclude = ('origin_content',)


class MovieBaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieInfo
        fields = ('id', 'title', 'desc', 'post_type', 'front_image')
