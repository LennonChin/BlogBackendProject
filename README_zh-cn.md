# 前后端分离的博客项目-后端工程

博客已上线，欢迎浏览：[https://blog.coderap.com/](https://blog.coderap.com/)

> [English description](https://github.com/LennonChin/BlogBackendProject/blob/master/README.md)

> 该仓库存放了博客项目的后端代码，使用Django及Django Rest Framework搭建。

> 注：与该仓库配合的前端代码仓库链接在此[BlogBackendProject](https://github.com/LennonChin/Blog-Frontend-Project)，前端代码使用Vue.js + Vue-Router + iView.js实现。

## 控制台后端效果

### PC端

![Home Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/PC_1.png)

![Article List Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/PC_2.png)

![Add Article Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/PC_3.png)

![Add Article Page](https://github.com/LennonChin/BlogBackendProject/blob/master/media/PC_4.png)

### 手机端

![Mobile effect](https://github.com/LennonChin/BlogBackendProject/blob/master/media/MOBILE_1.png)

## 整体技术栈

1. Python环境：Python 3.6.2

2. 主要依赖

- [Django==1.10.8](https://github.com/django/django)
- [djangorestframework==3.6.3](https://github.com/encode/django-rest-framework)

> 注：更多技术栈依赖请查看`requirements.txt`文件

## 已实现的基本功能

后端项目已实现了19个接口，主要功能点如下：

1. 实现了三个栏目：文章、图集和摄影，分别对应了三种不同的展示方式；同时实现了时光轴存档栏目；
2. 实现了管理控制台中三个栏目的文章的发布，可以发布Markdown格式的文章（使用EditorMD编辑器）；
3. 评论功能，目前使用的方式是昵称+邮箱，首次评论时会验证邮箱（通过发送验证码）；
4. 实现了文章加密功能；
5. 实现了七牛云存储服务的对接，发布评论文章等操作会将图片数据上传至七牛云；目前项目内不提供相应的服务，如需要对接请自行购买七牛云存储对象服务；

> 注：项目内使用的xadmin、EditorMD等插件都进行了二次开发，为了和项目特定功能进行配合，所以请不要轻易更换插件。

## 接下来将实现

1. 接入GitHub、微信、微博、Facebook等第三方登录评论。
2. 增加更多的栏目。

## 如何使用

1. clone本项目；
2. 本地安装Python3及pip环境；
3. 安装virtualenv及virtualenvwrapper环境后，执行以下命令创建一个虚拟环境：

``` bash
# 创建工作空间
> mkvirtualenv BlogBackend
# 激活工作空间
> workon BlogBackend
# 切换工作目录到本项目的根目录下，安装依赖
> pip install -r requirements.txt
```

4. 接下来，如果你使用的是PyCharm作为开发环境，请修改其Project Interpreter为创建好的工作空间；
5. 在该项目中，敏感的账号信息并没有提供，而是存放在`private.py`文件中，这个文件也没有托管到仓库，所以你需要自己在`setting.py`文件同级目录创建一个`private.py`文件，其内容如下：

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 下午6:01
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : private.py
# @Software: PyCharm

# 站点Secret Key设置，即settings.py中的SECRET_KEY项
PRIVATE_SECRET_KEY = ''

# 数据库连接配置
DATABASE_CONFIG = {
    'ENGINE': '', # 数据库引擎
    'NAME': '', # 使用的数据库库名
    "USER": '', # 数据库用户名
    "PASSWORD": '', # 数据库密码
    "HOST": '', # 数据库地址
    'PORT': 3306, # 数据库端口，MySQL为3306
    'OPTIONS': {
        "init_command": "SET default_storage_engine=INNODB;",
    }
}

# 发送邮件服务器配置
EMAIL_CONFIG = {
    'EMAIL_HOST': "", # 邮件服务器地址
    'EMAIL_PORT': 25, # 邮件服务器端口，一般为25
    'EMAIL_HOST_USER': "", # 邮件服务器账号
    'EMAIL_HOST_PASSWORD': "", # 邮件服务器密码
    'EMAIL_USE_SSL': False, # 是否使用SSL加密连接，一般不使用
    'EMAIL_FROM': "" # 该项一般与EMAIL_HOST相同
}

# 七牛云相关配置
PRIVATE_QINIU_ACCESS_KEY = '' # 七牛云Access key
PRIVATE_QINIU_SECRET_KEY = '' # 七牛云Secret key
PRIVATE_QINIU_BUCKET_DOMAIN = '' # 七牛云Bucket域
PRIVATE_QINIU_BUCKET_NAME = '' # 七牛云Bucket名称

PRIVATE_MEDIA_URL_PREFIX = '' # 站点Media资源前缀网址，访问七牛云时使用的资源前缀
PRIVATE_SITE_BASE_URL = '' # 站点网址
```

关于上述配置中`SECRET_KEY`（`PRIVATE_SECRET_KEY`）可以使用系统自动生成的，也可以自己生成，生成方式如下：

```python
In [1]: from django.core.management import utils

In [2]: utils.get_random_secret_key()
Out[2]: '7%x-f2u#@q@ar$q(=_yauzx8i4$8u&5epa=w^tjfo@-mp3+!r1'
```

`SECRET_KEY`是在startproject时候生成的，最终引用的是上述代码，具体可以查看源码。

6. 配置以上内容后，使用下面的命令迁移表

```shell
> python manage.py makemigrations
> python manage.py migrate
```

> 注：如果迁移失败，可以按照user、material、base、user_operation、index、剩余模块的顺序迁移。

7. 接下来直接运行下面的脚本启动本项目即可：

```python
> python manage.py runserver 127.0.0.1:8000
```

默认情况下，如果你运行后启动的evelopment Server为`127.0.0.1:8000`，则提供的接口访问地址为`http://127.0.0.1:8000/api`，后台管理地址为`http://127.0.0.1:8000/xadmin`。

同时，如果想要让前端访问到后台的接口，需要在后台的基础配置-网站配置中填写站点信息，最重要的是需要填写`API接口BaseURL`项为你前端页面访问的接口API。

## 其他补充

在本项目中，对Markdown的转换处理，使用了Pygments和pymdownx两个第三方库，同时对这两个库做了定制化的扩展，扩展后的代码位于`apps/utils/HTMLFormatter`目录下，其中有一个测试文件可供测试。如果想使用这些高级扩展，你需要将`superfences.py`、`highlight.py`两个文件复制到你的虚拟环境下的pymdownx安装包中并覆盖源文件，如我的虚拟环境是`BlogBackend`，目录即为`virtualEnvs/BlogBackend/lib/python3.6/site-packages/pymdownx`；其次，需要将本项目`apps/utils/HTMLFormatter`目录下的`code.py`文件更名为`html.py`文件，然后将改名后的文件复制到你的虚拟环境下的pygments安装包中并覆盖源文件，如我目录为`virtualEnvs/BlogBackend/lib/python3.6/site-packages/pygments/formatters`。

如果你觉得过于复杂而不打算使用扩展，也可以直接运行，但无法使用本博客扩展支持Markdown的高级语法，示例页面：[关于本站扩展Markdown语法](https://blog.coderap.com/article/4 "关于本站扩展Markdown语法")。

## License

[Apache-2.0](https://opensource.org/licenses/Apache-2.0)

Copyright (c) 2016-present, LennonChin

