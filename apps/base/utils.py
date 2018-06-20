#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午5:41
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : utils.py
# @Software: PyCharm

from datetime import datetime
from random import choice
from django.core.mail import EmailMessage
from django.template import loader
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

from user.models import EmailVerifyRecord
from BlogBackendProject.private import PRIVATE_QINIU_ACCESS_KEY, PRIVATE_QINIU_SECRET_KEY, PRIVATE_QINIU_BUCKET_NAME, \
    PRIVATE_MEDIA_URL_PREFIX
from BlogBackendProject.settings import SITE_BASE_URL, MEDIA_URL_PREFIX, EMAIL_FROM
from utils.RelativeImageExtension import RelativeImageExtension
from utils.SpanTableExtension import SpanTableExtension


# Page分页
class CustomePageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


# Limit 分页
class CustomeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
    min_limit = 1
    min_offset = 0


# 生成验证码
def generate_code(length):
    """
    生成四位数字的验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(length):
        random_str.append(choice(seeds))

    return "".join(random_str)


# 发送邮件
def send_email(email_info, email, send_type="comment"):
    if send_type == "comment":
        random_str = generate_code(4)
        email_title = "Diomedes博客评论-验证邮箱，验证码：{0}".format(random_str)
        context = {
            'email_info': {
                'base_url': SITE_BASE_URL,
                'receive_name': email_info['receive_name'],
                'code': random_str
            }
        }
        email_body = loader.render_to_string('CommentCodeEmail.html', context)

        message = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        message.content_subtype = "html"  # Main content is now text/html
        send_status = message.send()
        if int(send_status) == 1:
            # 保存验证码
            email_record = EmailVerifyRecord()
            email_record.code = random_str
            email_record.email = email
            email_record.send_type = send_type
            email_record.send_time = datetime.utcnow()
            email_record.save()
            return int(send_status)
        else:
            return 0

    if send_type == 'reply_comment':
        email_title = "Diomedes博客评论-收到回复"
        context = {
            'email_info': email_info
        }
        email_body = loader.render_to_string('ReplyCommentEmail.html', context)

        message = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        message.content_subtype = "html"  # Main content is now text/html
        return message.send()


def generate_qiniu_random_filename(length):
    seeds = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    # 按年月来划分子路径
    now = datetime.now()
    filename = ''.join(choice(seeds) for i in range(length))
    filename = '{0}/{1}/{2}'.format(now.year, now.month, filename)
    return filename


def generate_qiniu_token(object_name, use_type, expire_time=600):
    """
    用于生成七牛云上传所需要的Token
    :param object_name: 上传到七牛后保存的文件名
    :param use_type: 操作类型
    :param expire_time: token过期时间，默认为600秒，即十分钟
    :return: 
    """
    bucket_name = PRIVATE_QINIU_BUCKET_NAME
    from qiniu import Auth
    # 需要填写你的 Access Key 和 Secret Key
    access_key = PRIVATE_QINIU_ACCESS_KEY
    secret_key = PRIVATE_QINIU_SECRET_KEY
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200'
    }
    token = q.upload_token(bucket_name, object_name, expire_time, policy)
    base_url = PRIVATE_MEDIA_URL_PREFIX

    return (object_name, token, base_url, expire_time)


# 关于Python Markdown使用Bleach过滤XSS风险的配置

#: List of allowed tags
ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'address',
    'area',
    'article',
    'aside',
    'audio',
    'b',
    'base',
    'bdi',
    'bdo',
    'big',
    'blockquote',
    'br',
    'button'
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'command',
    'dd',
    'del',
    'details',
    'div',
    'dfn',
    'dl',
    'dt',
    'em',
    'embed',
    'fieldset',
    'figcaption',
    'figure',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'h7',
    'head',
    'header',
    'hr',
    'i',
    'img',
    'input',
    'ins',
    'kbd',
    'keygen',
    'label',
    'legend',
    'li',
    'map',
    'mark',
    'menu',
    'nav',
    'object',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'param',
    'pre',
    'progress',
    'q',
    'rp',
    'rt',
    'ruby',
    's',
    'samp',
    'section',
    'select',
    'small',
    'source',
    'span',
    'strike',
    'strong',
    'style',
    'sub',
    'summary',
    'sup',
    'table',
    'tbody',
    'td',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'time',
    'tr',
    'track',
    'tt',
    'u',
    'ul',
    'var',
    'video',
    'wbr',
    'xmp',
]

#: Map of allowed attributes by tag
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'td': ['colspan', 'rowspan', 'align'],
    'th': ['colspan', 'rowspan', 'align'],
    '*': ['class', 'id', 'style', 'type', 'value', 'title']
}

#: List of allowed styles
ALLOWED_STYLES = ['*']

#: List of allowed protocols
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

# python markdown extension default
MARKDOWN_EXTENSIONS_DEFAULT = [
    'markdown.extensions.abbr',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.footnotes',
    'markdown.extensions.tables',
    'markdown.extensions.smart_strong',
    'markdown.extensions.admonition',
    'markdown.extensions.codehilite',
    'markdown.extensions.headerid',
    'markdown.extensions.meta',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
    'markdown.extensions.toc',
    'markdown.extensions.wikilinks'
]

# python markdown extension pymdownx
MARKDOWN_EXTENSIONS_PYMDOWNX = [
    'pymdownx.extra',
    'pymdownx.superfences',
    'pymdownx.magiclink',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences',
    'pymdownx.details',
    'pymdownx.highlight',
    'pymdownx.inlinehilite',
    'pymdownx.keys',
    'pymdownx.progressbar',
    'pymdownx.critic',
    'pymdownx.arithmatex'
]

# python markdown extension custom
MARKDOWN_EXTENSIONS_CUSTOM = [
    RelativeImageExtension({
        'base_urls': [
            MEDIA_URL_PREFIX
        ]
    }),
    SpanTableExtension()
]

MARKDOWN_EXTENSIONS = MARKDOWN_EXTENSIONS_DEFAULT + MARKDOWN_EXTENSIONS_PYMDOWNX + MARKDOWN_EXTENSIONS_CUSTOM

MARKDOWN_EXTENSION_CONFIGS = {
    'pymdownx.superfences': {
        'global_toolsbar': """
            {
                "shownum": {
                    "class": "shownum-class ivu-icon",
                    "id": "button-shownum",
                    "title": "显示或隐藏行号",
                    "text": "",
                    "icon": "i-icon-shownum",
                    "event": "onclick='toggleCodeNum(this)'"},
                "theme": {
                    "class": "theme-class ivu-icon",
                    "id": "button-theme",
                    "title": "切换代码明暗显示",
                    "text": "",
                    "icon": "i-icon-theme",
                    "event": "onclick='toggleCodeTheme(this)'"},
                "copy": {
                    "class": "copy-class ivu-icon",
                    "id": "button-copy",
                    "title": "复制代码到剪切板",
                    "text": "",
                    "icon": "i-icon-copy",
                    "event": "onclick='copyCode(this)'"},
                "break": {
                    "class": "break-class ivu-icon",
                    "id": "button-break",
                    "title": "代码自动换行",
                    "text": "",
                    "icon": "i-icon-break",
                    "event": "onclick='toggleBreakCode(this)'"},
                "fold": {
                    "class": "fold-class ivu-icon",
                    "id": "button-fold",
                    "title": "点击收起代码",
                    "text": "",
                    "icon": "i-icon-fold",
                    "event": "onclick='toggleFoldCode(this)'"
                }
            }
            """
    }
}
