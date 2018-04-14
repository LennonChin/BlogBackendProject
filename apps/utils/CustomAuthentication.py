#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/28 上午11:26
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : CustomAuthentication.py
# @Software: PyCharm

import base64
import calendar
from datetime import datetime

from rest_framework import authentication
from rest_framework import exceptions


class AnonymousBrowseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META.keys():
            raise exceptions.AuthenticationFailed('Illegal Request')

        token = request.META['HTTP_AUTHORIZATION']
        if not token:
            raise exceptions.AuthenticationFailed('Illegal Request')

        try:
            decode_time, decode_url = bytes.decode(base64.b64decode(token)).split('*')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Illegal Request')

        utc_second = calendar.timegm(datetime.utcnow().timetuple())

        if abs(int(decode_time) - int(utc_second)) > 60 * 5:
            raise exceptions.AuthenticationFailed('Illegal Request')

        local_path = '{0}{1}{2}'.format('https://', request.META['SERVER_NAME'], request.META['PATH_INFO'])
        if local_path != decode_url:
            raise exceptions.AuthenticationFailed('Illegal Request')

        return None