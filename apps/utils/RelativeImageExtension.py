#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 上午11:45
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : RelativeImageExtension.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import unicode_literals
import copy

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class RelativeImageExtension(Extension):
    """ Relative Images Extension """

    def __init__(self, configs, *args, **kwargs):
        """Initialize."""

        self.configs = copy.deepcopy(configs)
        super(RelativeImageExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        absolute_images = RelativeImagesTreeprocessor(md)
        absolute_images.config = self.configs
        md.treeprocessors.add("relativeimages", absolute_images, "_end")

        md.registerExtension(self)


class RelativeImagesTreeprocessor(Treeprocessor):
    """ Relative Images Treeprocessor """

    def run(self, root):
        imgs = root.getiterator("img")
        for image in imgs:
            if self.is_absolute(image.attrib["src"]):
                image.set("data-src", self.make_external(image.attrib["src"]))
                image.set("src", "")

    def make_external(self, url):
        temp_url = url
        base_urls = self.config["base_urls"]
        flag = False
        for base_url in base_urls:
            if url.startswith(base_url):
                flag = True
                break
        if not flag:
            return temp_url
        i = temp_url.find('://')
        if i > 0:
            temp_url = temp_url[i+3:]
            i = temp_url.find('/')
            if i > 0:
                return temp_url[i:]
        return url

    def is_absolute(self, link):
        if link.startswith('http'):
            return True
        return False


def makeExtension(configs={}):
    """ Return an instance of the AbsoluteImagesExtension """
    return RelativeImageExtension(configs=configs)


if __name__ == '__main__':
    import markdown
    text = """
![001.png](https://jianshu.com/a/b/001.png)
![abc.png](/c/d/abc.png)
![test.png](https://material.coderap.com/efg/hijk/test.png)
"""
    configs = {
        'base_urls': ["https://material.coderap.com"],
    }

    md = markdown.markdown(text, extensions=['markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                             RelativeImageExtension(configs)])
    print(md)
