#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 上午11:08
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from datetime import datetime, timedelta
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from .serializers import EmailSerializer, EmailVerifySerializer
from base.utils import send_email
from .models import EmailVerifyRecord
from user.models import GuestProfile


class EmailCodeViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    邮箱验证码
    """
    def get_serializer_class(self):
        if self.action == "list":
            # list时，serializer不需要验证Email的发送频率
            return EmailVerifySerializer
        elif self.action == "create":
            return EmailSerializer
        return EmailSerializer

    def list(self, request, *args, **kwargs):
        """
        验证邮箱验证码
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 验证结果
        """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)  # status 400

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        nick_name = serializer.validated_data['nick_name']

        if code is None:
            # 验证码未填写
            context = {
                "error": '请填写验证码'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            ten_minutes_ago = datetime.now() + timedelta(hours=0, minutes=30, seconds=0)
            code_record = EmailVerifyRecord.objects.filter(email=email, code=code)[0]
            if code_record:
                if code_record.send_time.replace(tzinfo=None) > ten_minutes_ago:
                    # 验证码过期
                    context = {
                        "error": '验证码已过期，请重试'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # 验证码通过，创建客人
                    guest_record = None
                    guest_records = GuestProfile.objects.filter(email=email)
                    if guest_records.count():
                        guest_record = guest_records[0]
                    if guest_record:
                        guest_record.nick_name = nick_name
                        guest_record.save()
                    else:
                        guest_record = GuestProfile()
                        guest_record.nick_name = nick_name
                        guest_record.email = email
                        guest_record.save()
                    context = {
                        "guest": guest_record.id
                    }
                    return Response(context, status.HTTP_202_ACCEPTED)
            else:
                # 无验证码记录
                context = {
                    "error": '验证码验证错误，请重试'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        发送邮箱验证码
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        email = serializer.validated_data["email"]
        nick_name = serializer.validated_data['nick_name']

        email_info = {
            'receive_name': nick_name
        }

        try:
            send_email_status = send_email(email_info, email=email, send_type='comment')
        except Exception as e:
            send_email_status = 0

        if send_email_status != 1:

            context = {
                "email": [
                    '发送邮件出错，请检查您的邮箱；如果依旧出错，请联系博主'
                ]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        else:
            context = {
                "email": email
            }
            return Response(context, status.HTTP_201_CREATED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)