import markdown
from django.db import models
import bleach, html
from base.utils import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES, ALLOWED_PROTOCOLS

from material.models import PostBaseInfo
from user.models import GuestProfile
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class CommentInfo(models.Model):
    """
    评论基本信息
    """
    post = models.ForeignKey(PostBaseInfo, null=False, blank=False, verbose_name='所属文章')
    author = models.ForeignKey(GuestProfile, null=True, blank=True, related_name="comments", verbose_name='作者')
    reply_to_author = models.ForeignKey(GuestProfile, null=True, blank=True, related_name="be_comments",
                                        verbose_name='被回复人')
    comment_level = models.IntegerField(default=0, verbose_name="评论级别", help_text="评论级别")
    parent_comment = models.ForeignKey("self", null=True, blank=True, related_name="sub_comment", verbose_name="根评论",
                                       help_text="根评论")
    reply_to_comment = models.ForeignKey("self", null=True, blank=True, related_name='reply_comment',
                                         verbose_name='父级评论')
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    unlike_num = models.IntegerField(default=0, verbose_name="反对数", help_text="反对数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    is_active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "评论基本信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return html.unescape(self.detail.formatted_content[:100])


class CommentDetail(models.Model):
    """
    评论详细信息
    """
    comment_info = models.OneToOneField(CommentInfo, null=True, blank=True, related_name='detail',
                                        verbose_name="基本信息",
                                        help_text="基本信息")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(null=True, blank=True, verbose_name="处理后内容", help_text="处理后内容")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        self.formatted_content = bleach.clean(
            markdown.markdown(self.origin_content, extensions=MARKDOWN_EXTENSIONS, extension_configs=MARKDOWN_EXTENSION_CONFIGS, lazy_ol=False), ALLOWED_TAGS,
            ALLOWED_ATTRIBUTES, ALLOWED_STYLES,
            ALLOWED_PROTOCOLS, False, False)
        super(CommentDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.comment_info.post.title

    class Meta:
        verbose_name = "评论详细信息"
        verbose_name_plural = verbose_name + '列表'
