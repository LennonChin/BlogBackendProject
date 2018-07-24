import markdown
import requests
import json
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from BlogBackendProject.settings import DOUBAN_API_URL
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class BookInfo(PostBaseInfo):
    """
    图书基本信息
    """
    DOUBAN_TYPE = (
        ("book", "图书"),
        ("movie", "电影")
    )
    book_image = models.ImageField(upload_to="book/image/%y/%m", null=True, blank=True, verbose_name="封面图",
                                   help_text="大图833*217，小图243*207")
    is_reading = models.BooleanField(default=False, verbose_name='是否正在阅读', help_text='是否正在阅读')
    read_precentage = models.FloatField(default=0.0, null=True, blank=True, verbose_name='阅读进度', help_text='阅读进度')
    douban_type = models.CharField(max_length=255, choices=DOUBAN_TYPE, null=True, blank=True, verbose_name="豆瓣资源类型",
                                   help_text="豆瓣资源类型")
    douban_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="豆瓣资源ID", help_text="豆瓣资源ID")
    douban_infos = models.TextField(null=True, blank=True, verbose_name='豆瓣信息', help_text='豆瓣信息')
    book_isbn10 = models.CharField(max_length=255, null=True, blank=True, verbose_name="isbn10", help_text="isbn10")
    book_isbn13 = models.CharField(max_length=255, null=True, blank=True, verbose_name="isbn13", help_text="isbn13")
    book_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="书名", help_text="书名")
    book_origin_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="本书原始名", help_text="本书原始名")
    book_author = models.CharField(max_length=255, null=True, blank=True, verbose_name="本书作者", help_text="本书作者")
    book_tags = models.CharField(max_length=255, null=True, blank=True, verbose_name="本书标签", help_text="本书标签")
    book_rating = models.CharField(max_length=10, null=True, blank=True, verbose_name="本书豆瓣评分", help_text="本书豆瓣评分")
    book_publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name="出版社", help_text="出版社")
    publish_date = models.CharField(max_length=30, null=True, blank=True, verbose_name="出版日期", help_text="出版日期")
    book_pages = models.CharField(max_length=20, null=True, blank=True, verbose_name="总页数", help_text="总页数")
    book_url = models.URLField(null=True, blank=True, verbose_name="本书豆瓣链接", help_text="本书豆瓣链接")
    book_api = models.URLField(null=True, blank=True, verbose_name="本书API链接", help_text="本书API链接")
    is_update_douban_info = models.BooleanField(default=False, verbose_name='是否更新', help_text='会自动更新所有未填写的豆瓣信息')

    def __str__(self):
        return self.book_name

    def save(self, *args, **kwargs):
        self.post_type = 'book'
        # 豆瓣信息
        if self.is_update_douban_info:
            douban_infos = requests.get(
                '{0}/{1}/{2}'.format(DOUBAN_API_URL, self.douban_type, self.douban_id))
            douban_infos_dict = json.loads(douban_infos.text)
            if douban_infos_dict:
                if not self.book_isbn10:
                    self.book_isbn10 = douban_infos_dict['isbn10']
                if not self.book_isbn13:
                    self.book_isbn13 = douban_infos_dict['isbn13']
                if not self.book_name:
                    self.book_name = douban_infos_dict['title']
                if not self.book_origin_name:
                    self.book_origin_name = douban_infos_dict['origin_title']
                if not self.book_author:
                    self.book_author = '，'.join(douban_infos_dict['author'])
                if not self.book_tags:
                    self.book_tags = '，'.join(item['name'] for item in douban_infos_dict['tags'])
                if not self.book_rating:
                    self.book_rating = douban_infos_dict['rating']['average']
                if not self.book_publisher:
                    self.book_publisher = douban_infos_dict['publisher']
                if not self.publish_date:
                    self.publish_date = douban_infos_dict['pubdate']
                if not self.book_pages:
                    self.book_pages = douban_infos_dict['pages']
                if not self.book_url:
                    self.book_url = douban_infos_dict['alt']
                if not self.book_api:
                    self.book_api = douban_infos_dict['url']
                self.douban_infos = douban_infos.text
            self.is_update_douban_info = False
        super(BookInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name + '列表'


class BookDetail(models.Model):
    """
    图书详细信息
    """
    LANGUAGE = (
        ("CN", "中文"),
        ("EN", "English")
    )
    language = models.CharField(null=True, blank=True, max_length=5, choices=LANGUAGE, verbose_name="文章详情语言类别", help_text="现暂时提供两种语言类别")
    book_info = models.ForeignKey(BookInfo, null=True, blank=True, related_name='details', verbose_name="内容",
                                  help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(null=True, blank=True, verbose_name="添加时间", help_text="添加时间")
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown(self.origin_content, extensions=MARKDOWN_EXTENSIONS,
                                                   extension_configs=MARKDOWN_EXTENSION_CONFIGS, lazy_ol=False)

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
    NOTE_TYPE = (
        ("1", "一级"),
        ("2", "二级"),
        ("3", "三级")
    )
    book = models.ForeignKey(BookInfo, null=True, blank=True, verbose_name='图书', help_text="图书")
    chapter = models.CharField(max_length=20, null=False, blank=False, default="", verbose_name="章节", help_text="所属章节")
    note_type = models.CharField(max_length=20, null=True, blank=True, choices=NOTE_TYPE, verbose_name="笔记级别",
                                 help_text="笔记级别")
    parent_note = models.ForeignKey("self", null=True, blank=True, verbose_name="父笔记", help_text="父笔记",
                                    related_name="sub_note")
    is_reading = models.BooleanField(default=False, verbose_name="是否正在阅读", help_text="是否正在阅读")
    is_completed = models.BooleanField(default=False, verbose_name="是否读完", help_text="是否读完")
    is_noted = models.BooleanField(default=False, verbose_name="笔记是否完成", help_text="笔记是否完成")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 手动设置类型
        self.post_type = 'book/note'
        super(BookNoteInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "图书笔记"
        verbose_name_plural = verbose_name + '列表'


class BookNoteDetail(models.Model):
    """
    图书笔记详细信息
    """
    LANGUAGE = (
        ("CN", "中文"),
        ("EN", "English")
    )
    language = models.CharField(null=True, blank=True, max_length=5, choices=LANGUAGE, verbose_name="文章详情语言类别", help_text="现暂时提供两种语言类别")
    book_note_info = models.ForeignKey(BookNoteInfo, null=True, blank=True, related_name='details', verbose_name="内容",
                                       help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(null=True, blank=True, verbose_name="添加时间", help_text="添加时间")
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown(self.origin_content, extensions=MARKDOWN_EXTENSIONS,
                                                   extension_configs=MARKDOWN_EXTENSION_CONFIGS, lazy_ol=False)
        super(BookNoteDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.book_note_info.title

    class Meta:
        verbose_name = "图书笔记详情"
        verbose_name_plural = verbose_name + '列表'


class BookResource(models.Model):
    book = models.ForeignKey(BookInfo, verbose_name=u"图书")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(max_length=100, upload_to="book/resource/%Y/%m", verbose_name=u"资源文件")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图书资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
