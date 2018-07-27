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
        fields = ('language', 'formatted_content', 'add_time', 'update_time')


# 笔记
class BookNoteDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNoteDetail
        fields = ('language', 'formatted_content', 'add_time', 'update_time')


class BookNoteBaseInfoSerializer2(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, book_note):
        if book_note.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book_note.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class BookNoteBaseInfoSerializer1(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    sub_note = BookNoteBaseInfoSerializer2(many=True)
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, book_note):
        if book_note.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book_note.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class BookBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()
    book_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, book):
        if book.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book.front_image)

    def get_book_image(self, book):
        if book.book_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book.book_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = BookInfo
        fields = (
        'id', 'title', 'en_title', 'desc', 'en_desc', 'category', 'tags', 'click_num', 'like_num', 'comment_num',
        'post_type', 'is_recommend', 'is_hot', 'is_banner', 'is_commentable', 'index', 'need_auth', 'front_image',
        'front_image_type', 'is_reading', 'read_precentage', 'add_time', 'douban_id', 'douban_type', 'douban_infos',
        'book_isbn10', 'book_isbn13', 'book_name', 'book_author', 'book_publisher', 'book_pages', 'book_url',
        'book_image', 'book_rating', 'book_tags')


class BookNoteBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    book = BookBaseInfoSerializer()
    sub_note = BookNoteBaseInfoSerializer1(many=True)
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, book_note):
        if book_note.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book_note.front_image)

    def get_need_auth(self, article):
        if article.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password', 'browse_password_encrypt')


# 图书基本信息
class BookDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()
    book_image = serializers.SerializerMethodField()
    license = LicenseSerializer()
    details = BookDetailSerializer(many=True)
    book_note = serializers.SerializerMethodField()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    def get_front_image(self, book):
        if book.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book.front_image)

    def get_book_image(self, book):
        if book.book_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, book.book_image)

    def get_book_note(self, serializer):
        book_notes_json = []
        book_notes = BookNoteInfo.objects.filter(book_id=serializer.id, note_type=1)
        if book_notes:
            book_notes_json = BookNoteBaseInfoSerializer(book_notes, many=True,
                                                         context={'request': self.context['request']}).data
        return book_notes_json

    class Meta:
        model = BookInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class BookNoteDetialInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    book = BookBaseInfoSerializer()
    license = LicenseSerializer()
    details = BookNoteDetialSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookNoteInfo
        exclude = ('browse_password', 'browse_password_encrypt')
