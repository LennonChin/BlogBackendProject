# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from movie.models import MovieInfo, MovieDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ('formatted_content',)


class MovieDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    detail = MovieDetailSerializer()

    class Meta:
        model = MovieInfo
        fields = '__all__'


class MovieBaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieInfo
        fields = ('id', 'title', 'desc', 'post_type', 'is_banner', 'front_image')



