# GitHub Actions 工作流配置说明

## 概述

这个工作流实现了以下功能：
1. 自动构建和部署 MkDocs 到 GitHub Pages
2. 检测修改的文件
3. 自动刷新腾讯云 CDN 缓存

## 配置步骤

### 1. 设置 GitHub Secrets

在你的 GitHub 仓库中，进入 `Settings` > `Secrets and variables` > `Actions`，添加以下 secrets：

- `TENCENT_SECRET_ID`: 腾讯云 API 密钥 ID
- `TENCENT_SECRET_KEY`: 腾讯云 API 密钥 Key
- `CDN_DOMAIN`: 你的 CDN 域名（例如：example.com）

### 2. 调整腾讯云地域

在 `.github/workflows/ci.yml` 文件中，根据你的腾讯云配置调整 `TENCENT_REGION`：

```yaml
env:
  TENCENT_REGION: ap-beijing  # 根据你的配置调整
```

常见地域值：
- `ap-beijing`: 北京
- `ap-shanghai`: 上海
- `ap-guangzhou`: 广州
- `ap-hongkong`: 香港
- `ap-singapore`: 新加坡

### 3. 工作流工作原理

1. **代码检出**: 检出代码并获取完整的 git 历史
2. **依赖安装**: 安装 Python 依赖和 MkDocs 插件
3. **部署**: 使用 `mkdocs gh-deploy --force` 部署到 gh-pages 分支
4. **文件检测**: 比较当前 commit 和上一个 commit，找出修改的文件
5. **CDN 刷新**: 将修改的文件转换为 CDN URL，调用腾讯云 API 刷新缓存

### 4. 支持的文件类型

工作流会自动检测以下文件类型的变化：
- `.md` (Markdown 文件，会转换为 .html)
- `.html` (HTML 文件)
- `.css` (样式文件)
- `.js` (JavaScript 文件)
- `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico` (图片文件)
- `.xml`, `.txt` (其他文件)

### 5. 故障排除

#### 如果 CDN 刷新失败

工作流会在失败时显示需要手动刷新的 URL 列表。你可以：

1. 登录腾讯云控制台
2. 进入 CDN 服务
3. 选择"刷新预热" > "URL 刷新"
4. 手动添加需要刷新的 URL

#### 常见问题

1. **权限错误**: 确保腾讯云 API 密钥有 CDN 刷新权限
2. **地域错误**: 确保 `TENCENT_REGION` 与你的 CDN 配置匹配
3. **域名错误**: 确保 `CDN_DOMAIN` 设置正确

### 6. 监控和日志

工作流执行后，你可以在 GitHub Actions 页面查看详细的执行日志，包括：
- 修改的文件列表
- 需要刷新的 CDN URL
- 腾讯云 API 调用结果
- 任务 ID 和请求 ID

### 7. 安全注意事项

- 腾讯云 API 密钥具有访问权限，请妥善保管
- 建议使用子账号的 API 密钥，并限制权限范围
- 定期轮换 API 密钥
- 监控 API 调用频率，避免超出限制

## 自定义配置

### 修改刷新区域

如果你需要刷新境外节点，可以修改 `.github/scripts/refresh_cdn.py` 中的：

```python
req.Area = 'overseas'  # 刷新境外加速节点
```

### 添加更多文件类型

在 `.github/workflows/ci.yml` 中修改文件类型检测：

```bash
grep -E '\.(md|html|css|js|png|jpg|jpeg|gif|svg|ico|xml|txt|pdf)$'
```

### 批量刷新限制

腾讯云 CDN 每次最多可提交 1000 条 URL，如果超过限制，工作流会自动分批处理。
