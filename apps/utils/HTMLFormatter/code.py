# -*- coding: utf-8 -*-
"""
    pygments.formatters.html
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for HTML output.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from __future__ import print_function
from pkg_resources import iter_entry_points, load_entry_point


import os
import sys
import os.path
import json
from json.decoder import JSONDecodeError

from pygments.formatter import Formatter
from pygments.token import Token, Text, STANDARD_TYPES
from pygments.util import get_bool_opt, get_int_opt, get_list_opt, \
    StringIO, string_types, iteritems

try:
    import ctags
except ImportError:
    ctags = None

__all__ = ['HtmlFormatter']

# 转义表
_escape_html_table = {
    ord('&'): u'&amp;',
    ord('<'): u'&lt;',
    ord('>'): u'&gt;',
    ord('"'): u'&quot;',
    ord("'"): u'&#39;',
}


def escape_html(text, table=_escape_html_table):
    """
        Escape &, <, > as well as single and double quotes for HTML.
        将所有敏感字符使用转义表进行转义
    """
    return text.translate(table)


def _get_ttype_class(ttype):
    fname = STANDARD_TYPES.get(ttype)
    if fname:
        return fname
    aname = ''
    while fname is None:
        aname = '-' + ttype[-1] + aname
        ttype = ttype.parent
        fname = STANDARD_TYPES.get(ttype)
    return fname + aname


# CSS文件模板
CSSFILE_TEMPLATE = '''\
td.linenos { background-color: #f0f0f0; padding-right: 10px; }
span.lineno { background-color: #f0f0f0; padding: 0 5px 0 5px; }
pre { line-height: 125%%; }
%(styledefs)s
'''

# 文档头
DOC_HEADER = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
  <title>%(title)s</title>
  <meta http-equiv="content-type" content="text/html; charset=%(encoding)s">
  <style type="text/css">
''' + CSSFILE_TEMPLATE + '''
  </style>
</head>
<body>
<h2>%(title)s</h2>

'''

# 包含CSS的文档头
DOC_HEADER_EXTERNALCSS = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
  <title>%(title)s</title>
  <meta http-equiv="content-type" content="text/html; charset=%(encoding)s">
  <link rel="stylesheet" href="%(cssfile)s" type="text/css">
</head>
<body>
<h2>%(title)s</h2>

'''

# 文档尾
DOC_FOOTER = '''\
</body>
</html>
'''


class HtmlFormatter(Formatter):
    r"""
    Format tokens as HTML 4 ``<span>`` tags within a ``<pre>`` tag, wrapped
    in a ``<div>`` tag. The ``<div>``'s CSS class can be set by the `cssclass`
    option.

    用于格式化tokens为一个HTML4的<span>标签，并且使用pre包裹，外层用div包裹，外层div的class可以通过cssclass 参数设置

    If the `linenos` option is set to ``"table"``, the ``<pre>`` is
    additionally wrapped inside a ``<table>`` which has one row and two
    cells: one containing the line numbers and one containing the code.

    linenos设置为table时，pre会被一个table包裹，这个table有一个行，该行有两个td，一个包含行号，一个包含代码，如下：

    Example:

    .. sourcecode:: html

        <div class="highlight" >
        <table><tr>
          <td class="linenos" title="click to toggle"
            onclick="with (this.firstChild.style)
                     { display = (display == '') ? 'none' : '' }">
            <pre>1
            2</pre>
          </td>
          <td class="code">
            <pre><span class="Ke">def </span><span class="NaFu">foo</span>(bar):
              <span class="Ke">pass</span>
            </pre>
          </td>
        </tr></table></div>

    (whitespace added to improve clarity). 空白用于改善可读写

    Wrapping can be disabled using the `nowrap` option. 可以通过nowrap选项控制来禁止包裹

    A list of lines can be specified using the `hl_lines` option to make these
    lines highlighted (as of Pygments 0.11).

    可以通过hl_lines选项来指定一个高亮的行列表（0.11版本开始）

    With the `full` option, a complete HTML 4 document is output, including
    the style definitions inside a ``<style>`` tag, or in a separate file if
    the `cssfile` option is given.

    full选项可以控制一个完整的HTML4文档输出，包含style标签，或者一个单独的css文件，这个文件的路径可以通过cssfile来指定

    When `tagsfile` is set to the path of a ctags index file, it is used to
    generate hyperlinks from names to their definition.  You must enable
    `lineanchors` and run ctags with the `-n` option for this to work.  The
    `python-ctags` module from PyPI must be installed to use this feature;
    otherwise a `RuntimeError` will be raised.

    当tagfile参数设置为ctags的索引文件，则可以生成从名称到定义的超链接跳转。必须开启lineanchors，并且需要使用-n选项来运行ctags，
    同时python-ctags模块必须安装，否则会报RuntimeError

    The `get_style_defs(arg='')` method of a `HtmlFormatter` returns a string
    containing CSS rules for the CSS classes used by the formatter. The
    argument `arg` can be used to specify additional CSS selectors that
    are prepended to the classes. A call `fmter.get_style_defs('td .code')`
    would result in the following CSS classes:

    get_style_defs方法用于返回一个包含CSS类的规则，arg参数用于指定附加的css选择器，这些选择器都是内置的，
    例如`fmter.get_style_defs('td .code')`会返回：

    .. sourcecode:: css

        td .code .kw { font-weight: bold; color: #00FF00 }
        td .code .cm { color: #999999 }
        ...

    If you have Pygments 0.6 or higher, you can also pass a list or tuple to the
    `get_style_defs()` method to request multiple prefixes for the tokens:

    如果使用0.6之后的版本，可以传入一个list或者tuple给`get_style_defs()`方法类指定多个前缀：
    （这个方法主要用于定制高亮CSS时可以传入我们自己的前缀类名，应用到所有子代）

    .. sourcecode:: python

        formatter.get_style_defs(['div.syntax pre', 'pre.syntax'])

    The output would then look like this:

    输出会是这样的：

    .. sourcecode:: css

        div.syntax pre .kw,
        pre.syntax .kw { font-weight: bold; color: #00FF00 }
        div.syntax pre .cm,
        pre.syntax .cm { color: #999999 }
        ...

    Additional options accepted:

    其他选项

    `nowrap`
        If set to ``True``, don't wrap the tokens at all, not even inside a ``<pre>``
        tag. This disables most other options (default: ``False``).

        设置为True时将不包裹tokens，这个选项设置为True会使很多其他选项无效

    `full`
        Tells the formatter to output a "full" document, i.e. a complete
        self-contained document (default: ``False``).

        是否输出一个完整的HTML文档

    `title`
        If `full` is true, the title that should be used to caption the
        document (default: ``''``).

        文档标题

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``). This option has no effect if the `cssfile`
        and `noclobber_cssfile` option are given and the file specified in
        `cssfile` exists.

        用于设置文档的styles标签，可以是一个字符串也可以是一个Styke子类。
        当cssfile和noclobber_cssfile被指定并且cssfile存在的时候失效。

    `noclasses`
        If set to true, token ``<span>`` tags will not use CSS classes, but
        inline styles. This is not recommended for larger pieces of code since
        it increases output size by quite a bit (default: ``False``).

        如果设置为True，span标签将不会使用关于css的class，而使用inline的样式，
        这个在大片的代码时并不推荐，因为会增大输出体积

    `classprefix`
        Since the token types use relatively short class names, they may clash
        with some of your own class names. In this case you can use the
        `classprefix` option to give a string to prepend to all Pygments-generated
        CSS class names for token types.
        Note that this option also affects the output of `get_style_defs()`.

        token使用的一些短的class名能会跟你的其他class冲突，通过本参数你可以指定一个类前缀来预处理Pygments生成的css类，
        这个选项将同时影响`get_style_defs()`的输出

    `cssclass`
        CSS class for the wrapping ``<div>`` tag (default: ``'highlight'``).
        If you set this option, the default selector for `get_style_defs()`
        will be this class.

        该类用于指定包裹代码块的div的class，这个div是整个代码块的顶层，包含行号和代码，默认是highlight，
        如果设置了这个选项，`get_style_defs()`方法默认的选择器将会变成这个类

        .. versionadded:: 0.9
           If you select the ``'table'`` line numbers, the wrapping table will
           have a CSS class of this string plus ``'table'``, the default is
           accordingly ``'highlighttable'``.

           如果使用table模式的line numbers实现，外层table标签会在这个css后加上'table'，默认是highlighttable

    `cssstyles`
        Inline CSS styles for the wrapping ``<div>`` tag (default: ``''``).
        inline 方式下的外层div的styles

    `prestyles`
        Inline CSS styles for the ``<pre>`` tag (default: ``''``).
        inline 方式下的pre的styles

        .. versionadded:: 0.11

    `cssfile`
        If the `full` option is true and this option is given, it must be the
        name of an external file. If the filename does not include an absolute
        path, the file's path will be assumed to be relative to the main output
        file's path, if the latter can be found. The stylesheet is then written
        to this file instead of the HTML file.

        如果full选项是True同时该选项给定了，该选项应该是一个外部文件的路径。如果是路径不是绝对路径，会使用主要文件的输出路径，
        如果能够找到该文件，css样式将会被写入到改文件，而不是写在HTML文件中。

        .. versionadded:: 0.6

    `noclobber_cssfile`
        If `cssfile` is given and the specified file exists, the css file will
        not be overwritten. This allows the use of the `full` option in
        combination with a user specified css file. Default is ``False``.

        如果cssfile指定了并且存在，css文件不会被覆盖。这个选项允许在使用full选项时，与用户指定的css文件进行合并。
        即cssfile指定的文件可能有内容，noclobber_cssfile设置为True时会在cssfile指定的文件中追加内容，而不是覆盖。

        .. versionadded:: 1.1

    `linenos`
        If set to ``'table'``, output line numbers as a table with two cells,
        one containing the line numbers, the other the whole code.  This is
        copy-and-paste-friendly, but may cause alignment problems with some
        browsers or fonts.  If set to ``'inline'``, the line numbers will be
        integrated in the ``<pre>`` tag that contains the code (that setting
        is *new in Pygments 0.8*).

        如果设置为table，输出的line numbers会使用表格实现，表格有一行两列，第一列为行号，第二列为代码，这种方式对复制粘贴比较友好，
        但可能会引发对其问题，比如代码换行时行号会对不齐。
        如果设置为inline，行号会直接放在pre标签中，会被包含在代码里。

        For compatibility with Pygments 0.7 and earlier, every true value
        except ``'inline'`` means the same as ``'table'`` (in particular, that
        means also ``True``).

        为了0.7及以前版本的兼容，inline和table是一样的，意味着这个选项一直都是True

        The default value is ``False``, which means no line numbers at all.

        这个选项默认是False，意味着没有行号

        **Note:** with the default ("table") line number mechanism, the line
        numbers and code can have different line heights in Internet Explorer
        unless you give the enclosing ``<pre>`` tags an explicit ``line-height``
        CSS property (you get the default line spacing with ``line-height:
        125%``).

        注：使用默认的table实现行号😎，行号和代码在IE浏览器中可能有不同的行高，除非你给定了pre标签一个指定的行高（默认行高是125%）

    `hl_lines`
        Specify a list of lines to be highlighted.

        指定一个高亮行号的集合

        .. versionadded:: 0.11

    `linenostart`
        The line number for the first line (default: ``1``).

        起始行号，默认为1

    `linenostep`
        If set to a number n > 1, only every nth line number is printed.

        行号间隔，即隔几行显示行号

    `linenospecial`
        If set to a number n > 0, every nth line number is given the CSS
        class ``"special"`` (default: ``0``).

        行号特殊的样式，默认是0，如果设置了值，每隔几行会给某一行一个单独的名为special的class类

    `nobackground`
        If set to ``True``, the formatter won't output the background color
        for the wrapping element (this automatically defaults to ``False``
        when there is no wrapping element [eg: no argument for the
        `get_syntax_defs` method given]) (default: ``False``).

        如果设置为True，不会给输出的内容添加背景色，默认为False
        如果没有包裹则该选项默认为False

        .. versionadded:: 0.6

    `lineseparator`
        This string is output between lines of code. It defaults to ``"\n"``,
        which is enough to break a line inside ``<pre>`` tags, but you can
        e.g. set it to ``"<br>"`` to get HTML line breaks.

        代码行之间的间隔符，默认为`\n`，可以满足在pre标签中进行换行，也可以设置为`<br>`来实现HTML层面的换行

        .. versionadded:: 0.7

    `lineanchors`
        If set to a nonempty string, e.g. ``foo``, the formatter will wrap each
        output line in an anchor tag with a ``name`` of ``foo-linenumber``.
        This allows easy linking to certain lines.

        当设置为非空值时，例如`foo`，会在每个输出的行上添加一个锚点，使用`name="foo-linenumber"`，这个可以实现行的链接

        .. versionadded:: 0.9

    `linespans`
        If set to a nonempty string, e.g. ``foo``, the formatter will wrap each
        output line in a span tag with an ``id`` of ``foo-linenumber``.
        This allows easy access to lines via javascript.

        如果设置为非空值，例如`foo`，会在每个输出的行上添加一个span标签，使用`id="foo-linenumber"`，这个可以实现行的链接

        .. versionadded:: 1.6

    `anchorlinenos`
        If set to `True`, will wrap line numbers in <a> tags. Used in
        combination with `linenos` and `lineanchors`.

        如果设置为True，会给行号添加一个a标签，和`linenos` and `lineanchors`联合使用

    `tagsfile`
        If set to the path of a ctags file, wrap names in anchor tags that
        link to their definitions. `lineanchors` should be used, and the
        tags file should specify line numbers (see the `-n` option to ctags).

        用于置顶ctags文件，用于在锚点标签上添加name属性以链接到其他的定义。`lineanchors`应该指定，同时tags文件应该指定行号。

        .. versionadded:: 1.6

    `tagurlformat`
        A string formatting pattern used to generate links to ctags definitions.
        Available variables are `%(path)s`, `%(fname)s` and `%(fext)s`.
        Defaults to an empty string, resulting in just `#prefix-number` links.

        一个字符串用于格式化ctags定义的链接，使用类似于`%(path)s`, `%(fname)s` 或者 `%(fext)s`的模式.
        默认为空，输出的ctags链接结果仅仅是一个`#prefix-number`链接

        .. versionadded:: 1.6

    `filename`
        A string used to generate a filename when rendering <pre> blocks,
        for example if displaying source code.

        用于设置在渲染pre块时生成文件，例如显示源代码。

        .. versionadded:: 2.1


    **Subclassing the HTML formatter**

    .. versionadded:: 0.7

    The HTML formatter is now built in a way that allows easy subclassing, thus
    customizing the output HTML code. The `format()` method calls
    `self._format_lines()` which returns a generator that yields tuples of ``(1,
    line)``, where the ``1`` indicates that the ``line`` is a line of the
    formatted source code.

    HTML formatter现在可以支持子类化，即自定义输出的HTML代码。`format()`方法会调用`self._format_lines()`，
    会人会一个元组yields生成器，包含``(1, line)``，其中1表示line变量在格式化文件中的是一个行。

    If the `nowrap` option is set, the generator is the iterated over and the
    resulting HTML is output.

    如果nowrap选项被设置了，生成器是一个迭代结束的，并且结果HTML为输出

    Otherwise, `format()` calls `self.wrap()`, which wraps the generator with
    other generators. These may add some HTML code to the one generated by
    `_format_lines()`, either by modifying the lines generated by the latter,
    then yielding them again with ``(1, line)``, and/or by yielding other HTML
    code before or after the lines, with ``(0, html)``. The distinction between
    source lines and other code makes it possible to wrap the generator multiple
    times.

    否则的话，`format()` 会调用 `self.wrap()`，会将输出的生成器再包裹一层。
    这个步骤会通过`_format_lines()`在第一个生成器中添加一些HTML代码，通过厚着生成的行，并且将它们yield为``(1, line)``
    同时/或者将其他的HTML代码yield为``(0, html)``。
    源代码和其他代码之间的区别使得多次包裹生成器成为可能

    The default `wrap()` implementation adds a ``<div>`` and a ``<pre>`` tag.

    默认的`wrap()`实现会添加div和pre标签


    A custom `HtmlFormatter` subclass could look like this:

    .. sourcecode:: python

        class CodeHtmlFormatter(HtmlFormatter):

            def wrap(self, source, outfile):
                return self._wrap_code(source)

            def _wrap_code(self, source):
                yield 0, '<code>'
                for i, t in source:
                    if i == 1:
                        # it's a line of formatted code
                        t += '<br>'
                    yield i, t
                yield 0, '</code>'

    This results in wrapping the formatted lines with a ``<code>`` tag, where the
    source lines are broken using ``<br>`` tags.

    After calling `wrap()`, the `format()` method also adds the "line numbers"
    and/or "full document" wrappers if the respective options are set. Then, all
    HTML yielded by the wrapped generator is output.

    在调用`wrap()`后，`format()`方法会添加行号，或者进行全文档的包裹，至此，所有被生成器包裹的HTML yield都输出了。
    """

    name = 'HTML'
    aliases = ['html']
    filenames = ['*.html', '*.htm']

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.title = self._decodeifneeded(self.title)
        # 语言
        self.language = self._decodeifneeded(options.get('language', ''))
        self.nowrap = get_bool_opt(options, 'nowrap', False)
        self.noclasses = get_bool_opt(options, 'noclasses', False)
        self.classprefix = options.get('classprefix', '')
        self.cssclass = self._decodeifneeded(options.get('cssclass', 'highlight'))
        self.cssstyles = self._decodeifneeded(options.get('cssstyles', ''))
        self.prestyles = self._decodeifneeded(options.get('prestyles', ''))
        self.cssfile = self._decodeifneeded(options.get('cssfile', ''))
        self.noclobber_cssfile = get_bool_opt(options, 'noclobber_cssfile', False)
        self.tagsfile = self._decodeifneeded(options.get('tagsfile', ''))
        self.tagurlformat = self._decodeifneeded(options.get('tagurlformat', ''))
        self.filename = self._decodeifneeded(options.get('filename', ''))

        # 关于ul和li添加的属性
        # 一开始就显示行号
        self.shownum = get_bool_opt(options, 'shownum', True)
        # 代码是否折行，默认为True
        self.linefeed = get_bool_opt(options, 'linefeed', True)
        # ul自定义的class，默认为ul-wrap
        self.ulclass = self._decodeifneeded(options.get('ulclass', 'highlight-ul'))
        # ul自定义的style
        self.ulstyles = self._decodeifneeded(options.get('ulstyles', ''))
        # 需要行号的ul的class，默认为numbered
        self.ulnumclass = self._decodeifneeded(options.get('ulnumclass', 'numbered'))

        # li自定义的class，默认为li-wrap
        self.liclass = self._decodeifneeded(options.get('liclass', 'li-wrap'))
        # li自定义的style
        self.listyles = self._decodeifneeded(options.get('listyles', ''))
        # 需要行号的li的class，默认为numbered，该选项用在并不是所有行都需要行号的情况下
        self.linumclass = self._decodeifneeded(options.get('linumclass', 'numbered'))

        # 检查ctags相关，这里的ctags是import的
        if self.tagsfile:
            if not ctags:
                raise RuntimeError('The "ctags" package must to be installed '
                                   'to be able to use the "tagsfile" feature.')
            # 生成ctags
            self._ctags = ctags.CTags(self.tagsfile)

        # 行号模式
        linenos = 'ul'  # options.get('linenos', 'ul')
        if linenos == 'inline':
            self.linenos = 2  # inline为2
        elif linenos == 'ul':
            self.linenos = 3  # ul为3
        elif linenos == 'table':
            # compatibility with <= 0.7
            self.linenos = 1
        else:
            self.linenos = 0  # 如果没有指定默认为0

        # 获取各种选项
        self.linenostart = abs(get_int_opt(options, 'linenostart', 1))
        self.linenostep = abs(get_int_opt(options, 'linenostep', 1))
        self.linenospecial = abs(get_int_opt(options, 'linenospecial', 0))
        self.nobackground = get_bool_opt(options, 'nobackground', False)
        self.lineseparator = options.get('lineseparator', '\n')
        self.lineanchors = options.get('lineanchors', '')
        self.linespans = options.get('linespans', '')
        self.anchorlinenos = options.get('anchorlinenos', False)
        self.hl_lines = set()

        # 高亮行号存起来
        hl_lines = self._decodeifneeded(options.get('hl_lines', '{}'))
        self.hl_line_nums = []
        try:
            self.hl_lines = json.loads(hl_lines)
            for index, color in self.hl_lines.items():
                try:
                    self.hl_line_nums.append(int(index))
                except ValueError:
                    pass
        except Exception:
            if isinstance(hl_lines, (str,)):
                self.hl_lines = hl_lines.split()
            elif isinstance(hl_lines, (list, tuple)):
                self.hl_lines = list(hl_lines)
            else:
                raise ValueError('Invalid type `hl_lines`; you must give a list or json serialize value')
            self.hl_line_nums = [int(x) for x in self.hl_lines]

        # 生成style样式
        self._create_stylesheet()

    def _get_css_class(self, ttype):
        """Return the css class of this token type prefixed with
        the classprefix option."""
        ttypeclass = _get_ttype_class(ttype)
        if ttypeclass:
            return self.classprefix + ttypeclass
        return ''

    def _get_css_classes(self, ttype):
        """Return the css classes of this token type prefixed with
        the classprefix option."""
        cls = self._get_css_class(ttype)
        while ttype not in STANDARD_TYPES:
            ttype = ttype.parent
            cls = self._get_css_class(ttype) + ' ' + cls
        return cls

    def _create_stylesheet(self):
        t2c = self.ttype2class = {Token: ''}
        c2s = self.class2style = {}
        for ttype, ndef in self.style:
            name = self._get_css_class(ttype)
            style = ''
            if ndef['color']:
                style += 'color: #%s; ' % ndef['color']
            if ndef['bold']:
                style += 'font-weight: bold; '
            if ndef['italic']:
                style += 'font-style: italic; '
            if ndef['underline']:
                style += 'text-decoration: underline; '
            if ndef['bgcolor']:
                style += 'background-color: #%s; ' % ndef['bgcolor']
            if ndef['border']:
                style += 'border: 1px solid #%s; ' % ndef['border']
            if style:
                t2c[ttype] = name
                # save len(ttype) to enable ordering the styles by
                # hierarchy (necessary for CSS cascading rules!)
                c2s[name] = (style[:-2], ttype, len(ttype))

    def get_style_defs(self, arg=None):
        """
        Return CSS style definitions for the classes produced by the current
        highlighting style. ``arg`` can be a string or list of selectors to
        insert before the token type classes.
        """
        if arg is None:
            arg = ('cssclass' in self.options and '.' + self.cssclass or '')
        if isinstance(arg, string_types):
            args = [arg]
        else:
            args = list(arg)

        def prefix(cls):
            if cls:
                cls = '.' + cls
            tmp = []
            for arg in args:
                tmp.append((arg and arg + ' ' or '') + cls)
            return ', '.join(tmp)

        styles = [(level, ttype, cls, style)
                  for cls, (style, ttype, level) in iteritems(self.class2style)
                  if cls and style]
        styles.sort()
        lines = ['%s { %s } /* %s */' % (prefix(cls), style, repr(ttype)[6:])
                 for (level, ttype, cls, style) in styles]
        if arg and not self.nobackground and \
                self.style.background_color is not None:
            text_style = ''
            if Text in self.ttype2class:
                text_style = ' ' + self.class2style[self.ttype2class[Text]][0]
            lines.insert(0, '%s { background: %s;%s }' %
                         (prefix(''), self.style.background_color, text_style))
        if self.style.highlight_color is not None:
            lines.insert(0, '%s.hll { background-color: %s }' %
                         (prefix(''), self.style.highlight_color))
        return '\n'.join(lines)

    def _decodeifneeded(self, value):
        if isinstance(value, bytes):
            if self.encoding:
                return value.decode(self.encoding)
            return value.decode()
        return value

    def _wrap_full(self, inner, outfile):
        if self.cssfile:
            if os.path.isabs(self.cssfile):
                # it's an absolute filename
                cssfilename = self.cssfile
            else:
                try:
                    filename = outfile.name
                    if not filename or filename[0] == '<':
                        # pseudo files, e.g. name == '<fdopen>'
                        raise AttributeError
                    cssfilename = os.path.join(os.path.dirname(filename),
                                               self.cssfile)
                except AttributeError:
                    print('Note: Cannot determine output file name, '
                          'using current directory as base for the CSS file name',
                          file=sys.stderr)
                    cssfilename = self.cssfile
            # write CSS file only if noclobber_cssfile isn't given as an option.
            try:
                if not os.path.exists(cssfilename) or not self.noclobber_cssfile:
                    cf = open(cssfilename, "w")
                    cf.write(CSSFILE_TEMPLATE %
                             {'styledefs': self.get_style_defs('body')})
                    cf.close()
            except IOError as err:
                err.strerror = 'Error writing CSS file: ' + err.strerror
                raise

            yield 0, (DOC_HEADER_EXTERNALCSS %
                      dict(title=self.title,
                           cssfile=self.cssfile,
                           encoding=self.encoding))
        else:
            yield 0, (DOC_HEADER %
                      dict(title=self.title,
                           styledefs=self.get_style_defs('body'),
                           encoding=self.encoding))

        for t, line in inner:
            yield t, line
        yield 0, DOC_FOOTER

    def _wrap_ullinenos(self, inner):
        """
        需要用ul将其包裹
        变为格式如下：
        <div class="cssclass" style="cssstyles">
            <pre style="prestyle">
                <span></span>
                <ul>
                    <li>... code area</li>
                    <li>... code area</li>
                    <li class="hll">... code area</li>
                    <li>... code area</li>
                    <li>... code area</li>
                    <li>... code area</li>
                </ul>
            </pre>
        </div>
        """
        fl = self.linenostart  # 行号起始
        sp = self.linenospecial  # 特殊行间隔数
        st = self.linenostep  # 行号间隔数
        nocls = self.noclasses  # 是否是无class模式

        # 高亮行号
        hls = self.hl_line_nums

        ulstyles = []

        # 处理样式
        if self.ulstyles:
            ulstyles.append(self.ulstyles)

        # 如果使用了无class模式，则手动添加公共样式
        if nocls:
            ulstyles.append('padding: 5px 5px 5px 40px !important')
            ulstyles.append('margin: 0')
            ulstyles.append('background: transparent')

        # ul头
        ul = '<ul'
        if nocls:
            if self.shownum:
                ulstyles.append('list-style:decimal')
            else:
                ulstyles.append('list-style:none')
            ulstyles = '; '.join(ulstyles)
            ul = ul + (ulstyles and (' style="%s"' % ulstyles)) + '>'
        else:
            if self.shownum:
                # 添加class="numbered"
                self.ulclass = '%s %s' % (self.ulclass, self.ulnumclass)
            ulstyles = '; '.join(ulstyles)
            ul = ul + (' class="%s"' % self.ulclass) + (ulstyles and (' style="%s"' % ulstyles)) + '>'

        yield 0, ul

        # 记录行号
        lncount = 0
        for t, line in inner:
            li = '<li'
            if t:
                lncount += 1
                liclasses = []
                listyles = []
                if nocls:
                    # 添加li基本样式
                    listyles.append('border-left:1px solid #ddd !important')
                    listyles.append('background: transparent')
                    listyles.append('padding: 5px!important')
                    listyles.append('margin:0 !important')
                    listyles.append('line-height:14px')
                    listyles.append('word-break: break-all')
                    listyles.append('word-wrap: break-word')
                # 高亮
                if lncount in hls:
                    if not nocls:
                        liclasses.append('hll')
                        highlight_color = self.style.highlight_color
                        if isinstance(self.hl_lines, (dict,)):
                            # 使用用户自定义高亮
                            highlight_color = self.hl_lines[str(lncount)]
                            if highlight_color is not None:
                                listyles.append('background-color: %s' % (highlight_color, ))
                            else:
                                listyles.append('background-color: %s' % (highlight_color,))
                    else:
                        highlight_color = self.style.highlight_color
                        if isinstance(self.hl_lines, (dict,)):
                            highlight_color = self.hl_lines[str(lncount)]
                            if highlight_color is not None:
                                listyles.append('background-color: %s' % (highlight_color, ))
                            else:
                                listyles.append('background-color: %s' % (highlight_color,))
                        else:
                            # 使用默认高亮
                            listyles.append('background-color: %s' % (highlight_color,))
                # 间隔行
                if lncount >= fl and (lncount - fl) % st == 0:
                    # 添加行号
                    if not nocls:
                        liclasses.append('numbered')
                    else:
                        listyles.append('list-style: decimal-leading-zero;')
                else:
                    # 去除行号
                    if nocls:
                        listyles.append('list-style:none')

                # 特殊行
                if sp > 0 and lncount % sp == 0:
                    if not nocls:
                        liclasses.append('special')
                    else:
                        listyles.append('color: #999')
                else:
                    if nocls:
                        listyles.append('color: #222')

                # 不能添加class情况下是否折行需要特殊处理
                if self.linefeed:
                    if nocls:
                        listyles.append('white-space: pre-wrap')
                else:
                    if nocls:
                        listyles.append('white-space: pre')

                # 组合
                liclasses = ' '.join(liclasses)
                listyles = ';'.join(listyles)

                li = li + (liclasses and (' class="%s"' % liclasses)) + (listyles and (' style="%s"' % listyles)) + '>'

                yield 0, "%s%s</li>" % (li, line)
        # ul尾
        yield 0, '</ul>\n'

    def _wrap_tablelinenos(self, inner):
        dummyoutfile = StringIO()
        lncount = 0
        for t, line in inner:
            if t:
                lncount += 1
            dummyoutfile.write(line)

        fl = self.linenostart  # 行号起始
        mw = len(str(lncount + fl - 1))  # 最大行号宽度
        sp = self.linenospecial  # 特殊行间隔数
        st = self.linenostep  # 行号间隔数
        la = self.lineanchors  # 行锚点名称
        aln = self.anchorlinenos  # 如果设置为True，会给行号添加一个a标签，和`linenos` and `lineanchors`联合使用
        nocls = self.noclasses  # 是否是无class模式
        if sp:
            lines = []

            for i in range(fl, fl + lncount):
                if i % st == 0:
                    if i % sp == 0:
                        # 特殊行号
                        if aln:
                            # 锚点
                            lines.append('<a href="#%s-%d" class="special">%*d</a>' %
                                         (la, i, mw, i))
                        else:
                            lines.append('<span class="special">%*d</span>' % (mw, i))
                    else:
                        if aln:
                            # 锚点
                            lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                        else:
                            lines.append('%*d' % (mw, i))
                else:
                    lines.append('')
            ls = '\n'.join(lines)
        else:
            lines = []
            for i in range(fl, fl + lncount):
                if i % st == 0:
                    if aln:
                        lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                    else:
                        lines.append('%*d' % (mw, i))
                else:
                    lines.append('')
            ls = '\n'.join(lines)

        # in case you wonder about the seemingly redundant <div> here: since the
        # content in the other cell also is wrapped in a div, some browsers in
        # some configurations seem to mess up the formatting...

        style = []
        if nocls:
            style.append('background-color: #f0f0f0')
            style.append('padding-right: 10px')

        clazz = []
        if self.cssclass:
            clazz.append('%stable' % self.cssclass)

        # 自动换行
        if self.linefeed:
            if not self.nocls:
                clazz.append('linefeed')

        clazz = ' '.join(clazz)
        style = '; '.join(style)

        if nocls:
            yield 0, ('<table class="%s">' % clazz +
                      '<tr><td><div class="linenodiv" '
                      'style="%s">' + style +
                      '<pre style="line-height: 125%">' +
                      ls + '</pre></div></td><td class="code">')
        else:
            yield 0, ('<table class="%s">' % clazz +
                      '<tr><td class="linenos"><div class="linenodiv"><pre>' +
                      ls + '</pre></div></td><td class="code">')
        yield 0, dummyoutfile.getvalue()
        yield 0, '</td></tr></table>'

    def _wrap_inlinelinenos(self, inner):
        # need a list of lines since we need the width of a single number :(
        lines = list(inner)
        sp = self.linenospecial
        st = self.linenostep
        num = self.linenostart
        mw = len(str(len(lines) + num - 1))

        if self.noclasses:
            if sp:
                for t, line in lines:
                    if num % sp == 0:
                        style = 'background-color: #ffffc0; padding: 0 5px 0 5px'
                    else:
                        style = 'background-color: #f0f0f0; padding: 0 5px 0 5px'
                    yield 1, '<span style="%s">%*s </span>' % (
                        style, mw, (num % st and ' ' or num)) + line
                    num += 1
            else:
                for t, line in lines:
                    yield 1, ('<span style="background-color: #f0f0f0; '
                              'padding: 0 5px 0 5px">%*s </span>' % (
                                  mw, (num % st and ' ' or num)) + line)
                    num += 1
        elif sp:
            for t, line in lines:
                yield 1, '<span class="lineno%s">%*s </span>' % (
                    num % sp == 0 and ' special' or '', mw,
                    (num % st and ' ' or num)) + line
                num += 1
        else:
            for t, line in lines:
                yield 1, '<span class="lineno">%*s </span>' % (
                    mw, (num % st and ' ' or num)) + line
                num += 1

    def _wrap_lineanchors(self, inner):
        s = self.lineanchors
        # subtract 1 since we have to increment i *before* yielding
        i = self.linenostart - 1
        for t, line in inner:
            if t:
                i += 1
                yield 1, '<a name="%s-%d"></a>' % (s, i) + line
            else:
                yield 0, line

    def _wrap_linespans(self, inner):
        s = self.linespans
        i = self.linenostart - 1
        for t, line in inner:
            if t:
                i += 1
                yield 1, '<span id="%s-%d">%s</span>' % (s, i, line)
            else:
                yield 0, line

    def _wrap_div(self, inner):
        """
        添加一个div wrapper
        """
        style = []
        if (self.noclasses and not self.nobackground and
                self.style.background_color is not None):
            # 添加背景色
            style.append('background: %s' % (self.style.background_color,))
        if self.cssstyles:
            # 添加自定义样式，cssstyles只对此处有效
            style.append(self.cssstyles)

        clazz = []
        if self.cssclass:
            clazz.append(self.cssclass)

        # 自动换行，table模式会加在table tag上，所以此处不加
        if self.linenos != 1:
            # 自动换行
            if self.linefeed:
                if not self.noclasses:
                    clazz.append('linefeed')

        clazz = ' '.join(clazz)
        style = '; '.join(style)

        yield 0, ('<div' + (clazz and ' class="%s"' % clazz) +
                  (style and (' style="%s"' % style)) + '>')

        for tup in inner:
            yield tup
        yield 0, '</div>\n'

    def _wrap_pre(self, inner):
        style = []

        # 处理样式
        if self.prestyles:
            style.append(self.prestyles)

        # 如果使用了无class模式，则手动添加一个line-height样式
        if self.noclasses:
            style.append('line-height: 125%')
        style = '; '.join(style)

        if self.filename:
            # 这里是用于引入外部源码文件时，添加一个文件链接的span
            yield 0, ('<span class="filename">' + self.filename + '</span>')

        # the empty span here is to keep leading empty lines from being
        # ignored by HTML parsers
        # 元组第一位的0变为标志位，1标志是代码区域，0标志是非代码区域
        yield 0, ('<pre' + (style and ' style="%s"' % style) + '><span></span>')
        for tup in inner:
            yield tup
        yield 0, '</pre>'

    def _format_lines(self, tokensource):
        """
        Just format the tokens, without any wrapping tags.
        Yield individual lines.
        """
        nocls = self.noclasses  # 为True时直接使用内联style
        lsep = self.lineseparator  # 行换行符，默认为'\n'
        # for <span style=""> lookup only
        getcls = self.ttype2class.get
        c2s = self.class2style
        escape_table = _escape_html_table
        tagsfile = self.tagsfile

        lspan = ''
        line = []
        for ttype, value in tokensource:
            if nocls:
                cclass = getcls(ttype)
                while cclass is None:
                    ttype = ttype.parent
                    cclass = getcls(ttype)
                cspan = cclass and '<span style="%s">' % c2s[cclass][0] or ''
            else:
                cls = self._get_css_classes(ttype)
                cspan = cls and '<span class="%s">' % cls or ''

            parts = value.translate(escape_table).split('\n')

            if tagsfile and ttype in Token.Name:
                filename, linenumber = self._lookup_ctag(value)
                if linenumber:
                    base, filename = os.path.split(filename)
                    if base:
                        base += '/'
                    filename, extension = os.path.splitext(filename)
                    url = self.tagurlformat % {'path': base, 'fname': filename,
                                               'fext': extension}
                    parts[0] = "<a href=\"%s#%s-%d\">%s" % \
                               (url, self.lineanchors, linenumber, parts[0])
                    parts[-1] = parts[-1] + "</a>"

            # for all but the last line
            for part in parts[:-1]:
                if line:
                    if lspan != cspan:
                        line.extend(((lspan and '</span>'), cspan, part,
                                     (cspan and '</span>'), lsep))
                    else:  # both are the same
                        line.extend((part, (lspan and '</span>'), lsep))
                    yield 1, ''.join(line)
                    line = []
                elif part:
                    yield 1, ''.join((cspan, part, (cspan and '</span>'), lsep))
                else:
                    yield 1, lsep
            # for the last line
            if line and parts[-1]:
                if lspan != cspan:
                    line.extend(((lspan and '</span>'), cspan, parts[-1]))
                    lspan = cspan
                else:
                    line.append(parts[-1])
            elif parts[-1]:
                line = [cspan, parts[-1]]
                lspan = cspan
                # else we neither have to open a new span nor set lspan

        if line:
            line.extend(((lspan and '</span>'), lsep))
            yield 1, ''.join(line)

    def _lookup_ctag(self, token):
        entry = ctags.TagEntry()
        if self._ctags.find(entry, token, 0):
            return entry['file'], entry['lineNumber']
        else:
            return None, None

    def _highlight_lines(self, tokensource):
        """
        Highlighted the lines specified in the `hl_lines` option by
        post-processing the token stream coming from `_format_lines`.
        """
        hls = self.hl_line_nums

        for i, (t, value) in enumerate(tokensource):
            if t != 1:
                yield t, value
            if i + 1 in hls:  # i + 1 because Python indexes start at 0, 此处的i其实就是行的索引
                if self.linenos != 'ul':  # 如果是ul方式则需要另外使用li进行高亮处理
                    if self.noclasses:
                        highlight_color = self.style.highlight_color
                        if isinstance(self.hl_lines, (dict,)):
                            highlight_color = self.hl_lines[str(i + 1)]
                        style = ''
                        if highlight_color is not None:
                            style = (' style="background-color: %s"' %
                                     (highlight_color,))
                        yield 1, '<span%s>%s</span>' % (style, value)
                    else:
                        highlight_color = ''
                        if isinstance(self.hl_lines, (dict,)):
                            highlight_color = self.hl_lines[str(i + 1)]
                        style = ''
                        yield 1, '<span class="hll"' + (highlight_color and ' style="background-color: %s"' % highlight_color) + '>%s</span>' % value
            else:
                yield 1, value

    def wrap(self, source, outfile):
        """
        Wrap the ``source``, which is a generator yielding
        individual lines, in custom generators. See docstring
        for `format`. Can be overridden.
        """
        return self._wrap_div(self._wrap_pre(source))

    def format_unencoded(self, tokensource, outfile):
        """
        The formatting process uses several nested generators; which of
        them are used is determined by the user's options.

        Each generator should take at least one argument, ``inner``,
        and wrap the pieces of text generated by this.

        Always yield 2-tuples: (code, text). If "code" is 1, the text
        is part of the original tokensource being highlighted, if it's
        0, the text is some piece of wrapping. This makes it possible to
        use several different wrappers that process the original source
        linewise, e.g. line number generators.
        """
        # format处理，这个方法会给代码关键字加上特定的class，或者style（取决于noclasses选项）
        source = self._format_lines(tokensource)

        # 处理高亮，在ul模式下我们需要手动处理高亮，将高亮添加到li上
        if self.hl_lines and self.linenos != 3:
            source = self._highlight_lines(source)

        # 如果需要进行wrap
        if not self.nowrap:

            # inline模式行号
            if self.linenos == 2:
                source = self._wrap_inlinelinenos(source)

            # 行锚点，会在每行代码最前面加上一个标签，格式如下`<a name="self.lineanchors-1"></a>`
            # self.lineanchors = 'myanchor'
            if self.lineanchors:
                source = self._wrap_lineanchors(source)

            # linespans 如果设置为非空值，例如`foo`，会在每个输出的行上添加一个span标签，使用`id="foo-linenumber"`，这个可以实现行的链接
            # 会为每行代码套上一个span，格式如下`<span id="self.linespans-8">...</span>`
            # self.linespans = 'myspan'
            if self.linespans:
                source = self._wrap_linespans(source)

            # 此处进行ul模式行号处理
            if self.linenos == 3:
                source = self._wrap_ullinenos(source)

            # 进wrap，会变成如下形式
            # <div class="cssclass" style="cssstyles">
            #   <pre style="prestyle">
            #       <span></span>
            #       ... 代码区域
            #   </pre>
            # </div>
            source = self.wrap(source, outfile)

            # table模式行号
            if self.linenos == 1:
                source = self._wrap_tablelinenos(source)

            # 全文档模式
            if self.full:
                source = self._wrap_full(source, outfile)

        for t, piece in source:
            outfile.write(piece)
