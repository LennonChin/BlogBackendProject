#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from material.models import MaterialCategory, MaterialTag, MaterialLicense, PostBaseInfo, MaterialBanner, \
    MaterialCamera, \
    MaterialPicture, MaterialCommentInfo, MaterialCommentDetail, MaterialSocial, MaterialMaster
from user.serializers import GuestSerializer
from user.models import GuestProfile

from BlogBackendProject.settings import MEDIA_URL_PREFIX, SITE_BASE_URL
from base.utils import send_email


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


class SingleLevelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTag
        fields = "__all__"


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialLicense
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCamera
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
    camera = CameraSerializer()

    class Meta:
        model = MaterialPicture
        fields = "__all__"


class CommentDetailSerializer(serializers.ModelSerializer):
    origin_content = serializers.CharField(write_only=True, label='原始内容')
    formatted_content = serializers.CharField(read_only=True)
    update_time = serializers.DateTimeField(required=False)

    class Meta:
        model = MaterialCommentDetail
        fields = ('origin_content', 'formatted_content', 'update_time')


# 子级评论排序
class OrderSubCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('add_time')[:10]
        return super(OrderSubCommentListSerializer, self).to_representation(data)


# 子级评论
class SubCommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()

    class Meta:
        list_serializer_class = OrderSubCommentListSerializer
        model = MaterialCommentInfo
        fields = "__all__"


# 评论详细信息
class CommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()
    sub_comment = SubCommentDetailInfoSerializer(many=True)

    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


# 评论基本信息
class CommentBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


# 创建评论使用的serializer
class CreateCommentSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        # 创建评论
        comment_info = MaterialCommentInfo.objects.create(**validated_data)
        # 处理评论详情
        comment_detail = MaterialCommentDetail.objects.create(comment_info=comment_info, **detail_data)
        # 修改根级评论数数据
        if comment_info.parent_comment_id:
            parent_comment = MaterialCommentInfo.objects.get(id=comment_info.parent_comment_id)
            parent_comment.comment_num += 1
            parent_comment.save()
        # 文章的评论数数据
        post = comment_info.post
        post.comment_num += 1
        post.save()
        # 评论成功后给被回复人发送邮件
        if comment_info.reply_to_author_id:
            guest = GuestProfile.objects.filter(id=comment_info.reply_to_author_id)[0]
            if guest and guest.is_subcribe and guest.email:
                # 取出评论人
                author = GuestProfile.objects.filter(id=comment_info.author_id)[0]
                # 取出被回复评论
                reply_to_comment_detail = MaterialCommentDetail.objects.filter(comment_info_id=comment_info.reply_to_comment_id)[0]
                email_info = {
                    'base_url': SITE_BASE_URL,
                    'receive_name': guest.nick_name,
                    'post_title': post.title,
                    'post_url': '{0}/{1}/{2}'.format(SITE_BASE_URL, post.post_type, post.id),
                    'comment': reply_to_comment_detail.formatted_content if reply_to_comment_detail else '',
                    'reply_author_name': author.nick_name if author else '',
                    'reply_comment': comment_detail.formatted_content,
                    'unsubscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'unsubscribe', guest.uuid),
                    'subscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'subscribe', guest.uuid),
                }
                try:
                    send_email(email_info, guest.email, send_type='reply_comment')
                except Exception as e:
                    pass

        return comment_info

    class Meta:
        model = MaterialCommentInfo
        fields = "__all__"


class MaterialPostBaseInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()

    def get_front_image(self, post):
        if post.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, post.front_image)

    class Meta:
        model = PostBaseInfo
        fields = (
            'id', 'title', 'desc', 'tags', 'like_num', 'comment_num', 'click_num', 'front_image', 'front_image_type',
            'is_hot',
            'is_recommend', 'is_banner', 'is_commentable',
            'post_type', 'browse_password_encrypt', 'add_time')


class MaterialBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBanner
        fields = "__all__"


class MaterialSocialSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, social):
        if social.image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, social.image)

    class Meta:
        model = MaterialSocial
        fields = ('id', 'name', 'image', 'url', 'desc')


class MaterialMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialMaster
        fields = "__all__"