# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from rest_framework import serializers

from .models import SiteInfo, BloggerInfo, NavigationLink, FriendLink
from material.serializers import MaterialMasterSerializer, MaterialSocialSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class NavigationLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = NavigationLink
        fields = "__all__"


class SiteInfoSerializer(serializers.ModelSerializer):
    navigations = NavigationLinkSerializer(many=True)
    icon = serializers.SerializerMethodField()

    def get_icon(self, site_info):
        return "{0}/{1}".format(MEDIA_URL_PREFIX, site_info.icon)

    class Meta:
        model = SiteInfo
        fields = ('name', 'name_en', 'desc', 'icon', 'navigations', 'copyright', 'icp')


class BloggerInfoSerializer(serializers.ModelSerializer):
    socials = MaterialSocialSerializer(many=True)
    masters = MaterialMasterSerializer(many=True)

    class Meta:
        model = BloggerInfo
        fields = "__all__"


class FriendLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendLink
        fields = "__all__"
