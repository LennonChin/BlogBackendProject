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
        test_body = "<div><includetail><table width='800'border='0'align='center'cellpadding='0'cellspacing='0'bgcolor='#ffffff'style='font-family:'Microsoft YaHei';'><tbody><tr><td><table width='800'border='0'align='center'cellpadding='0'cellspacing='0'height='40'></table></td></tr><tr><td><table width='800'border='0'align='center'cellpadding='0'cellspacing='0'bgcolor='#409EFF'height='48'style='font-family:'Microsoft YaHei';'><tbody><tr><td width='74'height='48'border='0'align='center'valign='middle'style='padding-left:20px;'><a href=''target='_blank'><img src='https://img.alicdn.com/tps/TB1VnimLpXXXXcJapXXXXXXXXXX-80-19.png'width='80'height='19'border='0'></a></td><td width='703'height='48'colspan='2'align='right'valign='middle'style='color:#ffffff; padding-right:20px;'><a href=''target='_blank'style='color:#ffffff;text-decoration:none;font-family:'Microsoft YaHei';'>首页</a>&nbsp;&nbsp;<span style='color:#fff;'>|</span>&nbsp;&nbsp;<a href=''target='_blank'style='color:#ffffff;text-decoration:none;font-family:'Microsoft YaHei';'>文章</a>&nbsp;&nbsp;<span style='color:#fff;'>|</span>&nbsp;&nbsp;<a href=''target='_blank'style='color:#ffffff;text-decoration:none;font-family:'Microsoft YaHei';'>图集</a>&nbsp;&nbsp;<span style='color:#fff;'>|</span>&nbsp;&nbsp;<a href=''target='_blank'style='color:#ffffff;text-decoration:none;font-family:'Microsoft YaHei';'>摄影</a>&nbsp;&nbsp;<span style='color:#fff;'>|</span>&nbsp;<a href=''target='_blank'style='color:#ffffff;text-decoration:none;'>时间轴</a></td></tr></tbody></table></td></tr><tr><td><table width='800'border='0'align='left'cellpadding='0'cellspacing='0'style=' border:1px solid #edecec; border-top:none; border-bottom:none; padding:0 20px;font-size:14px;color:#333333;'><tbody><tr><td width='760'height='56'border='0'align='left'colspan='2'style=' font-size:16px;vertical-align:bottom;'>您好，Jerry：</td></tr><tr><td width='760'height='30'border='0'align='left'colspan='2'>&nbsp;</td></tr><tr><td width='40'height='32'border='0'align='left'valign='middle'style=' width:40px; text-align:left;vertical-align:middle; line-height:32px; float:left;'></td><td width='720'height='32'border='0'align='left'style=' width:720px; text-align:left;vertical-align:middle;line-height:32px;'>您的验证码是：123456</td></tr><tr><td width='720'height='32'colspan='2'style='padding-left:40px;'>&nbsp;</td></tr><tr><td width='720'height='32'colspan='2'style='padding-left:40px;'>&nbsp;</td></tr><tr><td width='720'height='14'colspan='2'style='padding-bottom:16px; border-bottom:1px dashed #e5e5e5;font-family:'Microsoft YaHei';'>Diomedes博客</td></tr><tr><td width='720'height='14'colspan='2'style='padding:8px 0 28px;color:#999999; font-size:12px;font-family:'Microsoft YaHei';'>此为系统邮件请勿回复</td></tr></tbody></table></td></tr><tr><td><table width='800'height='100'border='0'align='center'cellpadding='0'cellspacing='0'><tbody><tr><td width='800'height='100'align='center'valign='middle'><img border='0'height='100'src='https://img.alicdn.com/tfs/TB1LQ01RpXXXXXiXpXXXXXXXXXX-800-100.jpg'></td></tr></tbody></table></td></tr></tbody></table></includetail></div><style type='text/css'>body{margin:0 auto;padding:0;font-family:Microsoft Yahei,Tahoma,Arial;color:#333333;background-color:#fff;font-size:12px}a{color:#00a2ca;line-height:22px;text-decoration:none}a:hover{text-decoration:underline;color:#00a2ca}td{font-family:'Microsoft YaHei'}</style>"
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