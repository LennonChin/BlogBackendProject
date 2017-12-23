# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from .models import AlbumInfo, AlbumPhoto
from material.serializers import SingleLevelCategorySerializer, TagSerializer, PictureSerializer


class AlbumDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumPhoto
        fields = "__all__"


class AlbumDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    pictures = PictureSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = AlbumInfo
        fields = "__all__"


class AlbumBaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumInfo
        fields = ('id', 'title', 'author', 'click_num', 'like_num', 'comment_num', 'post_type', 'front_image',
                  'front_image_type', 'add_time')
