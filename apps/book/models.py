import markdown
from datetime import datetime
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo


# Create your models here.


class BookInfo(PostBaseInfo):
    """
    图书基本信息
    """
    DOUBAN_TYPE = (
        ("book", "图书"),
        ("movie", "电影")
    )
    douban_type = models.CharField(max_length=255, choices=DOUBAN_TYPE, null=True, blank=True, verbose_name="豆瓣资源类型",
                                   help_text="豆瓣资源类型")
    douban_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="豆瓣资源ID", help_text="豆瓣资源ID")
    isbn10 = models.CharField(max_length=255, null=True, blank=True, verbose_name="isbn10", help_text="isbn10")
    isbn13 = models.CharField(max_length=255, null=True, blank=True, verbose_name="isbn13", help_text="isbn13")
    book_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="书名", help_text="书名")
    book_author = models.CharField(max_length=255, null=True, blank=True, verbose_name="本书作者", help_text="本书作者")
    publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name="出版社", help_text="出版社")
    pages = models.CharField(max_length=20, null=True, blank=True, verbose_name="总页数", help_text="总页数")

    def get_book_chapter(self):
        return self.bookchapter_set.all()

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class BookDetail(models.Model):
    """
    图书详细信息
    """
    book_info = models.OneToOneField(BookInfo, null=True, blank=True, related_name='detail', verbose_name="内容",
                                     help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")

    def save(self, *args, **kwargs):
        self.formatted_content = markdown.markdown(self.origin_content,
                                                   extensions=[
                                                       'markdown.extensions.extra',
                                                       'markdown.extensions.codehilite',
                                                       'markdown.extensions.toc'
                                                   ])
        super(BookDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.book_info.title

    class Meta:
        verbose_name = "图书详情"
        verbose_name_plural = verbose_name + '列表'


class BookNoteInfo(PostBaseInfo):
    """
    图书笔记基本信息
    """

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "图书笔记"
        verbose_name_plural = verbose_name + '列表'


class BookNoteDetail(models.Model):
    """
    图书笔记基本信息
    """
    book_note_info = models.OneToOneField(BookNoteInfo, null=True, blank=True, related_name='detail', verbose_name="内容",
                                          help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")

    def save(self, *args, **kwargs):
        self.formatted_content = markdown.markdown(self.origin_content,
                                                   extensions=[
                                                       'markdown.extensions.extra',
                                                       'markdown.extensions.codehilite',
                                                       'markdown.extensions.toc'
                                                   ])
        super(BookNoteDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.book_note_info.title

    class Meta:
        verbose_name = "图书笔记详情"
        verbose_name_plural = verbose_name + '列表'


class BookChapter(BookNoteInfo):
    book = models.ForeignKey(BookInfo, verbose_name=u"图书")

    class Meta:
        verbose_name = u"图书章次"
        verbose_name_plural = verbose_name

    def get_learn_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.title


class BookSection(BookNoteInfo):
    chapter = models.ForeignKey(BookChapter, verbose_name=u"章")

    class Meta:
        verbose_name = u"图书节次"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class BookResource(models.Model):
    book = models.ForeignKey(BookInfo, verbose_name=u"图书")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(max_length=100, upload_to="book/resource/%Y/%m", verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图书资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
