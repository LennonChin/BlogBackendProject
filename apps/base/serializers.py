# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from rest_framework import serializers

from .models import BloggerInfo, FriendLink
from material.serializers import MaterialMasterSerializer, MaterialSocialSerializer


class BloggerInfoSerializer(serializers.ModelSerializer):
    socials = MaterialSocialSerializer(many=True)
    masters = MaterialMasterSerializer(many=True)

    class Meta:
        model = BloggerInfo
        fields = "__all__"


class FriendLinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendLink
        fields = "__all__"