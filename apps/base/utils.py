#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午5:41
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : utils.py
# @Software: PyCharm

from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

from random import Random
from random import choice
from django.core.mail import send_mail

from user.models import EmailVerifyRecord
from BlogBackendProject.settings import EMAIL_FROM


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
def send_email(email, send_type="comment"):

    random_str = generate_code(4)
    if send_type == "comment":
        random_str = generate_code(4)

    if send_type == "comment":
        email_title = "评论-激活邮箱"
        email_body = "您的验证码是：{0}".format(random_str)
        send_status = "1"#send_mail(email_title, email_body, EMAIL_FROM, [email])
        if int(send_status) == 1:
            print('验证码：' + random_str)
            # 保存验证码
            email_record = EmailVerifyRecord()
            email_record.code = random_str
            email_record.email = email
            email_record.send_type = send_type
            email_record.save()
            return int(send_status)