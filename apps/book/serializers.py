# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from .models import BookInfo, BookDetail, BookNoteInfo, BookNoteDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer, LicenseSerializer
from BlogBackendProject.settings import MEDIA_URL_PREFIX


# 图书详细信息
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = ('formatted_content', 'add_time', 'update_time')


# 笔记
class BookNoteDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNoteDetail
        fields = ('formatted_content', 'add_time', 'update_time')


class BookNoteBaseInfoSerializer2(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password',)


class BookNoteBaseInfoSerializer1(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    sub_note = BookNoteBaseInfoSerializer2(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)
    front_image = serializers.SerializerMethodField()

    def get_front_image(self, book_note):
        if book_note.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book_note.front_image)

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password',)


class BookBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()

    def get_front_image(self, book):
        if book.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book.front_image)

    class Meta:
        model = BookInfo
        fields = ('id', 'title', 'en_title', 'desc', 'en_desc', 'category', 'tags', 'click_num', 'like_num', 'comment_num', 'post_type', 'is_recommend', 'is_hot', 'is_banner', 'is_commentable',
                  'browse_password_encrypt', 'front_image', 'front_image_type', 'is_reading', 'read_precentage', 'add_time', 'douban_id', 'douban_type', 'douban_infos', 'book_isbn10', 'book_isbn13', 'book_name', 'book_author', 'book_publisher', 'book_pages', 'book_url', 'book_image', 'book_rating', 'book_tags')


class BookNoteBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    book = BookBaseInfoSerializer()
    sub_note = BookNoteBaseInfoSerializer1(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password',)


# 图书基本信息
class BookDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    details = BookDetailSerializer(many=True)
    book_note = serializers.SerializerMethodField()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    def get_book_note(self, serializer):
        book_notes_json = []
        book_notes = BookNoteInfo.objects.filter(book_id=serializer.id, note_type=1)
        if book_notes:
            book_notes_json = BookNoteBaseInfoSerializer(book_notes, many=True,
                                                         context={'request': self.context['request']}).data
        return book_notes_json

    class Meta:
        model = BookInfo
        exclude = ('browse_password',)


class BookNoteDetialInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    book = BookBaseInfoSerializer()
    license = LicenseSerializer()
    details = BookNoteDetialSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password',)
