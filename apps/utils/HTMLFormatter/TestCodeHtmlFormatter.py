#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 上午11:45
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : TestCodeHtmlFormatter.py
# @Software: PyCharm

"""
修改了文件：
pymdownx:
    superfences.py
    highlight.py
Pygments
    formater/html.py
    
global还可以这样用：
    - 自定义标题，全局工具栏：toolsbar='{"title": "This is a Special Title", "global":true}'
    - 自定义标题，自定义工具栏：toolsbar='{"title": "This is a Special Title","copy":{"class":"class_1","id":"id_1","title":"自定义按钮1","text":"自定义按钮1","icon":"i-icon-1","event":"onclick='alert(1)'"},"wrap":{"class":"class_2","id":"id_2","title":"自定义按钮2","text":"自定义按钮2","icon":"i-icon-2","event":"onclick='alert(2)'"},"fold":{"class":"class_3","id":"id_3","title":"自定义按钮3","text":"自定义按钮3","icon":"i-icon-3","event":"onclick='alert(3)'"}}'
    - 全局工具栏和标题：toolsbar="global"
"""

import markdown

if __name__ == '__main__':

    text = """
下面是上面提到的几种加载方式的测试：



```java linenums="0 5 2" hl_lines="1 3 5" toolsbar='{"title": "This is a Special Title", "global":true}' folded="1" linefeed="1"
package com.coderap.foundation.resource;

public class ResourceTest {

	public static void main(String[] args) {

		new ResourceTest().testGetPath();
	}

}
```

> 注2：`ClssLoader.getSystemResource(path)`等价于`ClassLoader.getSystemClassLoader().getResource(path)`。

需要注意的几点：

1. `Class.getResource("")`：返回的是当前类所在包开始的为置；
2. `Class.getResource("/")`：返回的是classpath的位置；

- classpath；
- 当前工程主目录，可以使用`System.getProperty("user.dir")`获取，但不推荐使用，会带来移植问题；

# 1 ======

## 1.1 ========

[=65% "65%"]

[=25%]{: .thin}

++ctrl+alt+delete++

"""

    extension_configs = {
        'pymdownx.superfences': {
            'global_toolsbar': """
            {
                "title": "这是一个标题",
                "copy": {
                    "class": "copy_class",
                    "id": "button-copy",
                    "title": "Click to copy code",
                    "text": "Copy",
                    "icon": "i-icon-copy",
                    "event": "onclick='copyCode(this)'"},
                "break": {
                    "class": "break_class",
                    "id": "button-break",
                    "title": "Click to break or no break line",
                    "text": "Break",
                    "icon": "i-icon-break",
                    "event": "onclick='breakCode(this)'"},
                "fold": {
                    "class": "fold_class",
                    "id": "button-fold",
                    "title": "Click to fold code",
                    "text": "Fold",
                    "icon": "i-icon-fold",
                    "event": "onclick='foldCode(this)'"
                }
            }
            """
        }
    }

    md = markdown.markdown(text, extensions=[
        'markdown.extensions.abbr',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.footnotes',
        'markdown.extensions.tables',
        'markdown.extensions.smart_strong',
        'markdown.extensions.admonition',
        'markdown.extensions.headerid',
        'markdown.extensions.meta',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
        'markdown.extensions.toc',
        'markdown.extensions.wikilinks',
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
        'pymdownx.arithmatex'], extension_configs=extension_configs, lazy_ol=False)
    print(md)
