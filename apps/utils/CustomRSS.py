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
    title = "Diomedes博客RSS订阅"
    link = "/rss/"
    description = "Diomedes博客RSS订阅，更新推送"

    def items(self):
        return PostBaseInfo.objects.order_by('-add_time')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc