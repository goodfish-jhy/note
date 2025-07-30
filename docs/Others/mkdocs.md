# MkDocs搭建个人笔记本

## 0.前言

本文旨在引导新手从零开始搭建一个部署于 GitHub Pages 的 MkDocs 个人笔记本，对于具体实现效果可以参考 [Home-GoodFish的笔记本](https://note.goodfish.site)。

需要注意的是，本教程偏向于在线笔记本而非博客，关于MkDocs搭建博客还请移步他处。

## 1.简介

在开始搭建之前，我们先来了解一下MkDocs是什么，以便读者对其能有较为整体的认识。

MkDocs 是一款轻量级的静态网站生成工具，专门用于快速搭建简洁易用的文档网站。它的核心目标是让用户专注于写作，而非技术细节。笔者只需通过简单的 Markdown 格式编写内容，MkDocs 就能自动将其转换为美观的网页，并支持自定义主题、导航菜单和扩展功能。

其适合如下场景：

 - 个人知识库：整理技术笔记、读书摘要、学习心得，随时在线查阅。
 - 小型团队共享：统一管理项目文档或协作教程，保持信息透明。
 - 开源项目：替代复杂文档框架，低成本维护清晰的说明页面。

!!! Abstract
    MkDocs 以极简主义的设计理念，解决了传统文档工具的臃肿问题。它不仅满足了“随手记录，便捷发布”的核心需求，还通过可定制化和自动化能力，成为构建个人在线笔记本的性价比之选。

## 2.配置环境

读者请确保当前电脑环境下有可正常使用的 Python3 环境，具体安装过程此处不过多赘述，可自行搜索教程。

请读者自行创建一个文件夹，后续文件存放在该文件夹下，并在这一目录下打开命令行。

为防止不同项目之间存在依赖冲突，读者可以通过创建虚拟环境来避免。当然，这一步并非必须。

```bash
# 创建名为 .venv 的虚拟环境（可修改）

python -m venv .venv

```

如果一切正常，此时目录下应该会多出一个名为 `.venv` 的文件夹，其内存放的便是虚拟环境。若笔者修改了虚拟环境名称，此处的名称也会改变，下文将默认虚拟环境名为`.venv`。

接下来，通过下方命令激活虚拟环境：

```bash
# Windows (CMD/PowerShell)：
.venv/Scripts/activate.bat

# Linux/macOS：
source .venv/bin/activate
```

如果激活成功，命令行前会出现 `(.venv)` 标识。

至此，虚拟环境配置就结束了。

------

MkDocs 是 Python 的一个包，可直接使用 `pip install mkdocs` 安装。

随后使用`pip install mkdocs-material` 安装 mkdocs-material，这是 MkDocs 的一个主题，本网站就是基于这一主题，接下来也将以这一主题为示范。

```bash
mkdocs new test    # 创建一个名为 test 的文件夹,存储网站相关文件
cd test
```

此时目录结构（忽略虚拟环境）

```text
.
└── test
    ├── docs # 存放MarkDown文件目录
    │   └── index.md # 主页
    └── mkdocs.yml # MkDocs配置文件
```

打开实时渲染服务（默认端口 8000），并且使用 watchdog 监控文件夹内的更改，在更改文件后自动刷新页面。

```bash
mkdocs serve
```

在浏览器中输入 `127.0.0.1:8000` 预览，终端键入 ++ctrl+c++ 关闭。

## 3.MkDocs配置

这边提供一份MkDocs配置文件的参考，其包含部分参考内容，请根据实际需要配置

```yaml
# ====================== 基础配置 ======================
site_name: "My Docs"  # 【必填】文档主标题名称，显示在左上角和浏览器标签页
site_url: "https://example.com"  # 最终的网站URL，用于生成绝对链接和sitemap
repo_url: "https://github.com/username/repo"  # 对应的GitHub仓库链接，用于右上角图标链接
edit_url: "https://github.com/username/repo/edit/master/docs/"  # 文档编辑链接，设置后会显示"编辑此页"按钮

site_description: "My project documentation"  # 站点描述，用于SEO元数据
site_author: "John Doe"  # 作者信息，用于主题页脚或SEO
copyright: "Copyright © 2023 John Doe"  # 左下角版权信息，支持HTML标签

# ====================== 主题配置 ======================
theme:
  name: "material"  # 使用Material主题
  language: "zh"  # 界面语言，中文设为"zh"
  
  # 图标配置
  icon:
    logo: "images/logo.svg"  # 左上角logo，支持SVG/PNG
    favicon: "images/favicon.ico"  # 网站图标
  
  # 自定义主题目录（用于覆盖模板文件）
  custom_dir: "theme_overrides"
  
  # 主题功能开关
  features:
    - "navigation.tabs"  # 启用顶部标签页导航
    - "navigation.indexes"  # 允许目录索引页
    - "toc.integrate"  # 集成目录到侧边栏
  
  # 字体配置
  font:
    text: "Roboto"  # 正文字体
    code: "Roboto Mono"  # 代码字体
  
  # 配色方案
  palette: 
    - scheme: "default"  # 默认配色方案
      primary: "indigo"  # 主色
      accent: "pink"  # 强调色
      toggle:
        icon: "material/toggle-switch"  # 主题切换图标
        name: "Switch to dark mode"  # 提示文字
    
    - scheme: "slate"  # 深色模式配色
      primary: "blue"
      accent: "lime"
      toggle:
        icon: "material/toggle-switch-off"
        name: "Switch to light mode"

# ====================== Markdown扩展 ======================
markdown_extensions:
  # 内置扩展
  - admonition  # 支持提示框（!!! note）
  - toc:  # 目录生成
      permalink: true  # 显示段落链接符号
      baselevel: 2  # 从h2开始生成目录
  
  # 第三方扩展（需安装pymdown-extensions）
  - pymdownx.superfences:  # 增强代码块
      custom_fences:  # 自定义代码块类型
        - name: "mermaid"
          class: "mermaid"
          format: !!python/name:pymdownx.superfences.fence_code_format
  
  - pymdownx.emoji:  # emoji支持
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

# ====================== 额外资源 ======================
extra_css:  # 附加CSS文件
  - "stylesheets/extra.css"  # 相对路径
  - "https://example.com/external.css"  # 外部URL

extra_javascript:  # 附加JS文件（加载在body末尾）
  - "javascripts/extra.js"
  - "https://example.com/external.js"

# ====================== 插件配置 ======================
plugins:
  - search  # 内置搜索插件
  
  - git-revision-date-localized:  # 显示最后修改时间
      type: "timeago"  # 显示为"3天前"格式
      timezone: "Asia/Shanghai"  # 时区设置
  
  - minify:  # 压缩HTML输出
      minify_html: true
      minify_js: true
      minify_css: true

# ====================== 导航配置 ======================
nav:
  - "首页": "index.md"  # 一级导航项
  
  - "用户指南":  # 二级导航分组
    - "安装指南": "guide/installation.md"
    - "配置说明": 
      - "基础配置": "guide/configuration/basic.md"
      - "高级配置": "guide/configuration/advanced.md"
  
  - "API参考": "api.md"  # 单独页面

# ====================== 额外配置 ======================
extra:
  # 社交链接（Material主题专用）
  social:
    - icon: "fontawesome/brands/github"  # 图标库+图标名
      link: "https://github.com/username"
      name: "GitHub"  # 悬停提示
    
    - icon: "fontawesome/brands/twitter"
      link: "https://twitter.com/username"
  
  # 分析工具配置
  analytics:
    provider: "google"
    property: "UA-XXXXX-Y"  # Google Analytics ID
  
  # 自定义变量（可在模板中使用）
  version: "1.0.0"
  release_date: "2023-01-01"

# ====================== 高级配置 ======================
docs_dir: "docs"  # 文档源文件目录（默认docs）
site_dir: "site"  # 输出目录（默认site）
strict: true  # 严格模式（警告视为错误）
use_directory_urls: true  # 使用目录式URL（如/page/而非/page.html）
watch: ["docs", "config.yml"]  # 开发服务器监听的文件变化
```