# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from article.models import ArticleInfo, ArticleDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer, LicenseSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleDetail
        fields = ('language', 'formatted_content', 'add_time', 'update_time')


class ArticleDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    details = ArticleDetailSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = ArticleInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class ArticleBaseInfoSerializer(serializers.ModelSerializer):
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
        model = ArticleInfo
        fields = (
            'id', 'title', 'en_title', 'desc', 'en_desc', 'author', 'tags', 'click_num', 'like_num', 'comment_num', 'post_type',
            'front_image', 'is_recommend', 'is_hot', 'is_banner', 'is_commentable', 'need_auth',
            'front_image_type', 'index', 'add_time')
