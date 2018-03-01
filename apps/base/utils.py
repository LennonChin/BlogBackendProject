#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午5:41
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : utils.py
# @Software: PyCharm

from datetime import datetime
from random import choice
from django.core.mail import send_mail, EmailMessage
from django.template import loader
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

from user.models import EmailVerifyRecord
from BlogBackendProject.private import PRIVATE_QINIU_ACCESS_KEY, PRIVATE_QINIU_SECRET_KEY, PRIVATE_QINIU_BUCKET_NAME, PRIVATE_MEDIA_URL_PREFIX
from BlogBackendProject.settings import EMAIL_FROM, SITE_BASE_URL


# 分页
class CustomePageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class CustomeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
    min_limit = 1
    min_offset = 0



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
def send_email(receive_name, email, send_type="comment"):

    random_str = generate_code(4)
    if send_type == "comment":
        random_str = generate_code(4)

    if send_type == "comment":
        email_title = "Diomedes博客评论-验证邮箱，验证码：{0}".format(random_str)
        email_content = "您的验证码是：{0}".format(random_str)
        email_body = loader.render_to_string('emailMessage.html', {
            'base_url': SITE_BASE_URL,
            'receive_name': receive_name,
            'email_context': email_content
        })

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
