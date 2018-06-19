# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from .models import AlbumInfo, AlbumPhoto
from material.serializers import SingleLevelCategorySerializer, TagSerializer, PictureSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class AlbumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumPhoto
        fields = "__all__"


class AlbumDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    pictures = PictureSerializer(many=True)
    tags = TagSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = AlbumInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class AlbumBaseInfoSerializer(serializers.ModelSerializer):
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, album):
        if album.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, album.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = AlbumInfo
        fields = ('id', 'title', 'en_title', 'desc', 'en_desc', 'author', 'click_num', 'like_num', 'comment_num', 'post_type', 'front_image', 'front_image_type', 'is_banner', 'is_commentable', 'need_auth', 'add_time')
