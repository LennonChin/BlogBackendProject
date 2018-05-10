#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 下午3:04
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : AbsoluteImageExtension.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import unicode_literals
from urllib.parse import urljoin
import copy

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class AbsoluteImageExtension(Extension):
    """ Absolute Images Extension """

    def __init__(self, configs, *args, **kwargs):
        """Initialize."""

        self.config = copy.deepcopy(configs)
        super(AbsoluteImageExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        absolute_images = AbsoluteImagesTreeprocessor(md)
        absolute_images.config = self.getConfigs()
        md.treeprocessors.add("absoluteimages", absolute_images, "_end")

        md.registerExtension(self)


class AbsoluteImagesTreeprocessor(Treeprocessor):
    """ Absolute Images Treeprocessor """

    def run(self, root):
        imgs = root.getiterator("img")
        for image in imgs:
            if self.is_relative(image.attrib["src"]):
                image.set("src", self.make_external(image.attrib["src"]))

    def make_external(self, path):
        return urljoin(self.config["base_url"][0], path)

    def is_relative(self, link):
        if link.startswith('http'):
            return False
        return True


def makeExtension(configs={}):
    """ Return an instance of the AbsoluteImagesExtension """
    return AbsoluteImageExtension(configs=configs)


if __name__ == '__main__':
    import markdown
    text = """
![001.png](/a/b/001.png)
![abc.png](/c/d/abc.png)
![test.png](/efg/hijk/test.png)
"""

    configs = {
        'base_url': ["https://comment.coderap.com"],
    }

    absoluteImagesExtension = AbsoluteImageExtension(configs)
    md = markdown.markdown(text, extensions=['markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                             absoluteImagesExtension])
    print(md)
