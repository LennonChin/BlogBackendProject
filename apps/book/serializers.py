# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from .models import BookInfo, BookDetail, BookChapter, BookSection, BookNoteInfo, BookNoteDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer, LicenseSerializer


# 图书详细信息
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = ('formatted_content',)


# 节
class BookSectonDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNoteDetail
        fields = ('formatted_content',)


class BookSectonDetialInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    detail = BookSectonDetialSerializer()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookSection
        exclude = ('browse_password',)


class BookSectonBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = BookSection
        exclude = ('browse_password',)


# 章
class BookChapterDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNoteDetail
        fields = ('formatted_content',)


class BookChapterDetialInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    detail = BookChapterDetialSerializer()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = BookChapter
        exclude = ('browse_password',)


class BookChapterBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    book_section = serializers.SerializerMethodField()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    def get_book_section(self, serializer):
        book_sections_json = []
        book_sections = BookSection.objects.filter(chapter_id=serializer.id)
        if book_sections:
            book_sections_json = BookSectonBaseInfoSerializer(book_sections, many=True,
                                                              context={'request': self.context['request']}).data
        return book_sections_json

    class Meta:
        model = BookChapter
        exclude = ('browse_password',)


# 图书基本信息
class BookDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    detail = BookDetailSerializer()
    book_chapter = serializers.SerializerMethodField()
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    def get_book_chapter(self, serializer):
        book_chapters_json = []
        book_chapters = BookChapter.objects.filter(book_id=serializer.id)
        if book_chapters:
            book_chapters_json = BookChapterBaseInfoSerializer(book_chapters, many=True,
                                                               context={'request': self.context['request']}).data
        return book_chapters_json

    class Meta:
        model = BookInfo
        exclude = ('browse_password',)


class BookBaseInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = BookInfo
        fields = ('id', 'title', 'desc', 'category', 'tags', 'post_type', 'is_recommend', 'is_hot', 'is_banner',
                  'browse_password_encrypt', 'front_image', 'add_time', "douban_id", 'isbn10', 'isbn13', 'book_name',
                  'book_author', 'publisher', 'pages',)
