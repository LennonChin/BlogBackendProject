# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from movie.models import MovieInfo, MovieDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer, LicenseSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ('language', 'formatted_content', 'add_time', 'update_time')


class MovieDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    details = MovieDetailSerializer(many=True)
    license = LicenseSerializer()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = MovieInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class MovieBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, movie):
        if movie.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, movie.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = MovieInfo
        fields = (
            'id', 'title', 'en_title', 'desc', 'en_desc', 'directors', 'actors', 'category', 'post_type',
            'is_recommend', 'is_hot',
            'is_banner', 'is_commentable', 'index', 'need_auth',
            'front_image', 'add_time')
