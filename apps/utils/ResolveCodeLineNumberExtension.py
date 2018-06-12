#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 上午11:45
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : ResolveCodeLineNumberExtension.py
# @Software: PyCharm

import copy, re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from markdown import Extension
from markdown.postprocessors import Postprocessor


class ResolveLineNumberPostprocessor(Postprocessor):

    @staticmethod
    def addUlTag1(matched):
        value = matched.group()
        return value

    @staticmethod
    def addUlTag(matched):
        value = matched.group()
        return value
        preEle = ET.fromstring(value)
        children = preEle.getchildren()
        if len(children) == 0 and children[0].tag == 'ul':
            return value
        else:
            # 创建ul
            ulEle = ET.Element('ul')
            for child in children:
                liEle = ET.SubElement(ulEle, 'li')
                liEle.append(child)
            # 清除preEle的所有元素
            preEle.clear()
            # 将新构建的元素添加到pre中
            preEle.append(ulEle)
        return str(ET.tostring(preEle))

    def run(self, text):
        pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.S | re.M)
        text = re.sub(pattern, ResolveLineNumberPostprocessor.addUlTag, text)
        return text


class ResolveCodeLineNumberExtension(Extension):
    def __init__(self, configs, *args, **kwargs):
        self.config = copy.deepcopy(configs)
        super(ResolveCodeLineNumberExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        resolve_line_number = ResolveLineNumberPostprocessor(md)
        resolve_line_number.config = self.getConfigs()
        md.postprocessors.add('resolve_line_number', resolve_line_number, "_end")
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return ResolveCodeLineNumberExtension(*args, **kwargs)


if __name__ == '__main__':
    import markdown

    text = """
下面是上面提到的几种加载方式的测试：

[=65% "65%"]

[=25%]{: .thin}

++ctrl+alt+delete++

??? danger "Java代码"
	```java hl_lines="1 3 5 6 7 8 9 10"
	package com.coderap.foundation.resource;

	public class ResourceTest {

		public static void main(String[] args) {

			new ResourceTest().testGetPath();
		}

		public void testGetPath() {

			System.out.println("---- this.getClass().getResource(\"\") ");
			System.out.println(this.getClass().getResource(""));
			System.out.println(this.getClass().getResource("").getPath());
			System.out.println();
		}
	}
	```

???+ info "Java代码"
	```java hl_lines="1 3 5 6 7 8 9 10"
	package com.coderap.foundation.resource;

	public class ResourceTest {

		public static void main(String[] args) {

			new ResourceTest().testGetPath();
		}

		public void testGetPath() {

			System.out.println("---- this.getClass().getResource(\"\") ");
			System.out.println(this.getClass().getResource(""));
			System.out.println(this.getClass().getResource("").getPath());
			System.out.println();
		}
	}
	```

???+ warning "Java代码"
	```java hl_lines="1 3 5 6 7 8 9 10"
	package com.coderap.foundation.resource;

	public class ResourceTest {

		public static void main(String[] args) {

			new ResourceTest().testGetPath();
		}

		public void testGetPath() {

			System.out.println("---- this.getClass().getResource(\"\") ");
			System.out.println(this.getClass().getResource(""));
			System.out.println(this.getClass().getResource("").getPath());
			System.out.println();
		}
	}
	```

???+ success "Java代码"
	```java hl_lines="1 3 5 6 7 8 9 10"
	package com.coderap.foundation.resource;

	public class ResourceTest {

		public static void main(String[] args) {

			new ResourceTest().testGetPath();
		}

		public void testGetPath() {

			System.out.println("---- this.getClass().getResource(\"\") ");
			System.out.println(this.getClass().getResource(""));
			System.out.println(this.getClass().getResource("").getPath());
			System.out.println();
		}
	}
	```

???+ success "对比代码块"
	```java hl_lines="1 3" tab=
	package com.coderap.foundation.resource;

	public class ResourceTest {

		public static void main(String[] args) {

			new ResourceTest().testGetPath();
		}

		public void testGetPath() {

			System.out.println("---- this.getClass().getResource(\"\") ");
			System.out.println(this.getClass().getResource(""));
			System.out.println(this.getClass().getResource("").getPath());
			System.out.println();
		}
	}
	```

	```C linenums="1 1 2" hl_lines="1 3" tab=
	#include 

	int main(void) {
	  printf("hello, world\n");
	}
	```

	```C++ linenums="1 1 2" hl_lines="1 3" tab=
	#include <iostream>

	int main() {
	  std::cout << "Hello, world!\n";
	  return 0;
	}
	```

	```C# linenums="1 1 2" hl_lines="1 3" tab=
	using System;

	class Program {
	  static void Main(string[] args) {
	    Console.WriteLine("Hello, world!");
	  }
	}
	```

> 注2：`ClssLoader.getSystemResource(path)`等价于`ClassLoader.getSystemClassLoader().getResource(path)`。

需要注意的几点：

1. `Class.getResource("")`：返回的是当前类所在包开始的为置；
2. `Class.getResource("/")`：返回的是classpath的位置；
3. `getClassLoader().getResource("")`：**返回的是classpath的位置**；
4. `getClassLoader().getResource("/")`：**错误用法**，会抛出`NullPointerException`错误。

Java中不存在标准的相对路径，各种相对路径取资源的方式都是基于某种规则转化为绝对路径，但是在编程过程中，绝对不要直接使用绝对路径。所以，我们在使用Java载入Resource资源时，只要寻找到合适的参考基点，就能很轻松得定位到要找的路径，一般情况下参考基点有如下几种：

- classpath；
- 当前工程主目录，可以使用`System.getProperty("user.dir")`获取，但不推荐使用，会带来移植问题；
- Web应用程序的根目录 ，在Web应用程序中，一般通过`ServletActionContext.getServletContext().getRealPath(“/”) `方法得到Web应用程序的根目录的绝对路径。


{--

```C# hl_lines="1 3"
using System;

class Program {
  static void Main(string[] args) {
    Console.WriteLine("Hello, world!");
  }
}
```

--}

{++

```C# hl_lines="1 3"
using System;

class Program {
  static void Main(string[] args) {
    Console.WriteLine("Hello, world!");
  }
}
```

++}

```java
package com.coderap.foundation.resource;

public class ResourceTest {

	public static void main(String[] args) {

		new ResourceTest().testGetPath();
	}

	public void testGetPath() {

		System.out.println("---- this.getClass().getResource(\"\") ");
		System.out.println(this.getClass().getResource(""));
		System.out.println(this.getClass().getResource("").getPath());
		System.out.println();
	}
}
```

# 1 ======

## 1.1 ========

### 1.1.1 =========

## 1.2 =======

### 1.2.1 =======

#### 1.2.1.1 =======
"""
    configs = {
    }

    md = markdown.markdown(text, extensions=[
        'markdown.extensions.abbr',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.footnotes',
        'markdown.extensions.tables',
        'markdown.extensions.smart_strong',
        'markdown.extensions.admonition',
        'markdown.extensions.codehilite',
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
        'pymdownx.arithmatex'], lazy_ol=False)
    print(md)
