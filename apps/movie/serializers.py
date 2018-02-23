# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from movie.models import MovieInfo, MovieDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ('formatted_content',)


class MovieDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    detail = MovieDetailSerializer()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = MovieInfo
        exclude = ('browse_password', )


class MovieBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    front_image = serializers.SerializerMethodField()

    def get_front_image(self, article):
        return "{0}/{1}".format(MEDIA_URL_PREFIX, article.front_image)

    class Meta:
        model = MovieInfo
        fields = (
            'id', 'title', 'desc', 'directors', 'actors', 'category', 'post_type', 'is_recommend', 'is_hot',
            'is_banner', 'browse_password_encrypt',
            'front_image', 'add_time')
