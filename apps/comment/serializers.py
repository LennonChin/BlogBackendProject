#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from .models import CommentInfo, CommentDetail
from material.models import PostBaseInfo
from user.serializers import GuestSerializer
from user.models import GuestProfile

from BlogBackendProject.settings import SITE_BASE_URL
from base.utils import send_email


class CommentLikeSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=True, label='评论')
    operation = serializers.BooleanField(required=True, label='like或者unlike')


class CommentDetailSerializer(serializers.ModelSerializer):
    origin_content = serializers.CharField(write_only=True, label='原始内容')
    formatted_content = serializers.CharField(read_only=True)
    update_time = serializers.DateTimeField(required=False)

    class Meta:
        model = CommentDetail
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
        model = CommentInfo
        fields = "__all__"


# 评论详细信息
class CommentDetailInfoSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()
    author = GuestSerializer()
    reply_to_author = GuestSerializer()
    sub_comment = SubCommentDetailInfoSerializer(many=True)

    class Meta:
        model = CommentInfo
        fields = "__all__"


# 评论基本信息
class CommentBaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentInfo
        fields = "__all__"


# 创建评论使用的serializer
class CreateCommentSerializer(serializers.ModelSerializer):
    detail = CommentDetailSerializer()

    def validate(self, attrs):
        # TODO 这里需要对评论的内容进行校验，包括评论内容，评论人，评论回复人等信息
        # 判断评论内容是否不为空
        if 'detail' not in attrs or 'origin_content' not in attrs['detail'] or len(attrs['detail']['origin_content']) == 0:
            raise serializers.ValidationError("请指定评论内容")
        # 判断评论级别
        # 判断文章是否存在，是否允许评论
        post = PostBaseInfo.objects.filter(id=attrs['post'].id)[0]
        if post is None:
            raise serializers.ValidationError("请指定文章信息")
        if not post.is_commentable:
            raise serializers.ValidationError("该文章暂不允许评论")
        else:
            return attrs

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        # 创建评论
        comment_info = CommentInfo.objects.create(**validated_data)
        # 处理评论详情
        comment_detail = CommentDetail.objects.create(comment_info=comment_info, **detail_data)
        # 修改根级评论数数据
        if comment_info.parent_comment_id:
            parent_comment = CommentInfo.objects.get(id=comment_info.parent_comment_id)
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
                reply_to_comment_detail = CommentDetail.objects.filter(comment_info_id=comment_info.reply_to_comment_id)[0]
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
        model = CommentInfo
        fields = "__all__"
