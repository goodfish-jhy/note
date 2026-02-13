# MkDocs搭建个人笔记本

## 0 前言

本文旨在引导新手从零开始搭建一个部署于 GitHub Pages 的 MkDocs 个人笔记本，对于具体实现效果可以参考 [Home-GoodFish的笔记本](https://note.goodfish.site)。

需要注意的是，本教程偏向于在线笔记本而非博客，关于MkDocs搭建博客还请移步他处。

## 1 简介

在开始搭建之前，我们先来了解一下MkDocs是什么，以便读者对其能有较为整体的认识。

MkDocs 是一款轻量级的静态网站生成工具，专门用于快速搭建简洁易用的文档网站。它的核心目标是让用户专注于写作，而非技术细节。笔者只需通过简单的 Markdown 格式编写内容，MkDocs 就能自动将其转换为美观的网页，并支持自定义主题、导航菜单和扩展功能。

其适合如下场景：

- 个人知识库：整理技术笔记、读书摘要、学习心得，随时在线查阅。
- 小型团队共享：统一管理项目文档或协作教程，保持信息透明。
- 开源项目：替代复杂文档框架，低成本维护清晰的说明页面。

!!! Abstract
    MkDocs 以极简主义的设计理念，解决了传统文档工具的臃肿问题。它不仅满足了“随手记录，便捷发布”的核心需求，还通过可定制化和自动化能力，成为构建个人在线笔记本的性价比之选。

## 2 配置环境

读者请确保当前电脑环境下有可正常使用的 Python3 环境，具体安装过程此处不过多赘述，可自行搜索教程。

请读者自行创建一个文件夹，后续文件存放在该文件夹下，并在这一目录下打开命令行。

### 2.1 创建虚拟环境（可选）

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

### 2.2 安装依赖

MkDocs 是一个基于 Python 的静态网站生成工具包，可通过 pip 包管理器直接安装。  

本网站采用 MkDocs 的官方主题 mkdocs-material 进行构建，后续示例也将基于该主题展开。  

安装命令如下：  

```bash
pip install mkdocs
pip install mkdocs-material
```

### 2.3 创建工作目录

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

## 3 MkDocs配置

### 3.1 参考配置文件

笔者在此提供一份MkDocs配置文件的参考，以便读者了解各配置项的功能

```yaml title="mkdocs.yml"
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

### 3.2 引用文件图标

需要注意的是，如果需要在配置文件当中引用本地文件，是以`docs`文件夹为根目录表示，例如：

- `\test\docs\assets\xxx.js` 应为 `assets\xxx.js`

对于 [Material Design Icons](https://pictogrammers.com/library/mdi/) 内的图标，可以使用 `material\xxxx` 的方式嵌入。

### 3.3 亮暗色切换

如果读者需要亮暗色切换，可以参考：

```yaml
theme:
  palette:
     # Palette toggle for automatic mode
    - media: "(prefers-color-scheme)"
      toggle:
        icon: material/theme-light-dark
        name: 切换到亮色模式

    # Palette toggle for light mode
    - media: "(prefers-color-scheme: light)"
      scheme: light_mode
      accent: light_mode
      primary: light_mode
      toggle:
        icon: material/weather-sunny
        name: 切换到暗色模式

    # Palette toggle for dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      accent: dark_mode
      primary: dark_mode
      toggle:
        icon: material/weather-night
        name: 切换到跟随系统设置
```

??? Warning "注意"
    这里的 `light_mode` 和 `dark_mode` 是笔者自定义的样式，不能直接使用，具体配置参考笔者github仓库中 `\docs\assets\stylesheets\extra.css`文件。

### 3.4 $\LaTeX$ 支持

使用 `MathJax` 嵌入即可实现。

``` yaml title="mkdocs.yml"
markdown_extensions:
  - pymdownx.arithmatex

extra_javascript:
  - https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML
```

由于 `MathJax` 的渲染速度较慢，可以考虑使用 $\KaTeX$ 进行替代。

需要注意的是，$\KaTeX$ 原生不支持美金符号包裹的语法，需要额外引用一个js脚本:

```js title="katex-autorender-init.js"
document.addEventListener("DOMContentLoaded", function() {
  renderMathInElement(document.body, {
      delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false},
          {left: '\\(', right: '\\)', display: false},
          {left: '\\[', right: '\\]', display: true}
      ],
      throwOnError: false
  });
});
```

## 4 MkDocs 部署

到这一步，读者应确保修改后的配置文件不存在错误，即在本地运行 `mkdcos serve` 可以正常预览效果。

对于MkDocs部署，可以选择部署在个人服务器或Github Page，下面将分别介绍。

### 4.1 部署到服务器

接下来，本文将详细阐述通过Docker容器进行应用部署的具体流程。在开始之前，需要准备一台可正常连接的服务器（关于云服务器的选购不在本文讨论范围内）。

#### 4.1.1 宝塔面板的安装

通过执行以下命令即可完成宝塔面板的一键安装。该命令会自动检测系统环境并选择合适的下载方式：

```bash
if [ -f /usr/bin/curl ];then curl -sSO https://download.bt.cn/install/install_panel.sh;else wget -O install_panel.sh https://download.bt.cn/install/install_panel.sh;fi;bash install_panel.sh ed8484bec
```

#### 4.2.2 安装Docker及镜像

安装完成后，登录宝塔面板并在左侧功能菜单中找到Docker选项。首次使用时系统会提示安装Docker服务，只需按照提示完成安装即可。

在Docker管理界面中搜索并安装Material for MkDocs镜像，安装完成后将本地项目文件完整上传至服务器指定目录即可完成部署。

关于域名配置和SSL证书等后续设置，都可以通过宝塔面板提供的可视化界面便捷地完成配置。

!!! Info "关于 git-revision-date-localized 插件"
    如果需要使用 `git-revision-date-localized` 插件实现显示创建和修改时间，需要在 GitHub 中同时维护一个储存库，这样插件才可以从 Git 记录中获取相关信息。

### 4.2 部署到Github Page

要部署到 Github Pages，只需在本地运行 `mkdocs gh-deploy` 命令即可自动将生成的静态网站部署到你的 GitHub 仓库的 `gh-pages` 分支，并通过 GitHub Pages 服务进行托管。

由于篇幅限制，GitHub账号注册不在本文探讨范围内。

#### 4.2.1 创建 GitHub仓库

在登录到 GitHub 账号之后，打开 [New repository](https://github.com/new) 页面创建新存储库。在此处可以配置你的仓库名、描述等信息。

创建好仓库之后就可以将其绑定到本地的工作目录了，若读者电脑没有安装 Git，可以到 [https://git-scm.com/downloads](https://git-scm.com/downloads) 下载。

#### 4.2.2 初始化 Git 仓库

在项目根目录下运行：

```bash
git init
git remote add origin https://github.com/你的用户名/你的仓库名.git
```

并将本地代码推送到 GitHub：

```bash
git add .
git commit -m "init mkdocs site"
git push -u origin master
```

#### 4.2.3 部署到 GitHub Pages

运行：

```bash
mkdocs gh-deploy
```

该命令会自动构建并推送 `site` 目录内容到 `gh-pages` 分支。

部署完成后，你可以通过 `https://你的用户名.github.io/你的仓库名/` 访问你的 MkDocs 网站。

#### 4.2.4 自定义域名

如需自定义域名，可在`docs`目录下添加 `CNAME` 文件并填写入域名，并在 GitHub Pages 设置中填写你的域名。

并在域名的dns解析界面中，创建对应的域名解析。

详细操作参考这篇[GitHub文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。

#### 4.2.5 通过 GitHub Action 实现自动部署

同时，还可以通过`GitHub Action`来实现在`git push`时自动推送到 `gh-pages`。

创建 `.github/workflows/ci.yml` 内容如下：

```yaml hl_lines="28" title="ci.yml"
name: ci 
on:
  push:
    branches:
      - master 
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v4
        with:
          python-version: "3.x"

      - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV 
      - uses: actions/cache@v3
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: .cache
          restore-keys: |
            mkdocs-material-
      - run: pip install mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin
      - run: mkdocs gh-deploy --force
```

需要将高亮的行中的依赖进行修改，修改为读者实际的环境依赖。

## 5 撰写文章

完成了上述配置之后，就可以开始撰写文章了。

在MkDocs中，所有文章均以MarkDown格式存储在`docs`文件夹下。

在完成了文章编辑后，不要忘记在`mkdocs.yml`中nav处添加文章（如果启用目录插件）。
