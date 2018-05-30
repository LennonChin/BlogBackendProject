#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 上午10:33
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : CustomRSS.py
# @Software: PyCharm

from django.contrib.syndication.views import Feed
from material.models import PostBaseInfo


class LatestEntriesFeed(Feed):
    title = "CODERAP博客RSS订阅"
    link = "/rss/"
    description = "Cast a cold eyes, one life one death, horseman pass by"

    def items(self):
        return PostBaseInfo.objects.filter(is_active=True).order_by('-add_time')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_extra_kwargs(self, item):
        return {
            'comments': '{}#comments'.format(item.get_absolute_url())
        }