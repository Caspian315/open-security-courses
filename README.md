# 开源安全精品课程

网安科协线下课程的公开资料主页。使用 MkDocs + Material，提供学期日程、课程目录、讲义、课件下载和历次开课记录。

**网站：<https://caspian315.github.io/open-security-courses/>**

当前内容为筹备版：课表、讲师、时间和地点待确认，Git 课程与下载资料均标注为示例。

## 本地预览

需要 Python 3.11 或以上版本。以下命令在**项目目录的 PowerShell**运行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
```

浏览器访问 <http://127.0.0.1:8000/>。保存文档后自动刷新；在终端按 `Ctrl+C` 停止预览。虚拟环境已创建并安装好依赖时，只需运行最后一条命令。

## 检查与构建

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe scripts/check_site.py
```

检查器验证生成网页中的站内链接、锚点、脚本、样式和下载文件，并检查 `/open-security-courses/` 子路径。构建产物放在 `site/`，不提交到 Git。

如需按线上子路径预览：

```powershell
.\.venv\Scripts\python.exe scripts/serve_site.py
```

访问 <http://127.0.0.1:8000/open-security-courses/>。

## 更新课程与资料

详细步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)。常见操作：

| 操作 | 修改位置 |
| --- | --- |
| 修改线下时间、地点或讲师 | `docs/schedule/<学期>/index.md`，同步对应开课页 |
| 新增课程 | `docs/courses/<方向>/<课程>/index.md`，并加入方向目录和 `mkdocs.yml` 导航 |
| 新增一次开课 | 在该课程目录新建 `<学期>.md`，在课程介绍和学期日程添加入口 |
| 上传小体积课件 | `docs/assets/materials/<学期>/<课程>/`，从开课页添加相对链接 |
| 发布大文件或录像 | 在开课页加入实际 GitHub Release 下载链接或视频原始链接 |

模板在 `templates/`。复制为实际页面后填写内容、补齐有效链接；新学期创建新文件，旧资料继续保留。正式发布前替换示例课表，补充真实的课程、讲师、地点、报名方式与公开联系方式。

## 自动发布

仓库启用 GitHub Pages，发布来源选择 **GitHub Actions**。

- Pull Request：安装锁定依赖，执行严格构建和站内链接检查。
- 合并或推送到 `main`：检查通过后上传 Pages artifact，并部署到 `github-pages` 环境。
- 手动发布：在 Actions 页面运行 `Build and deploy course site` 工作流。

失败的构建不会触发新部署。需要恢复已发布内容时，通过新的提交撤销有问题的修改，再由工作流重新发布。

工作流会按仓库所有者和仓库名设置站点 URL；迁移仓库后，还需更新 `mkdocs.yml` 中的默认 `site_url`、`repo_url`、`repo_name`，以及文档中的项目链接。以后使用自定义域名时，同步配置 Pages 域名和 `COURSE_SITE_URL`。

## 文件组织

```text
docs/
  index.md                       首页
  schedule/<学期>/index.md       本学期日程
  schedule/archive.md            历史日程入口
  courses/<方向>/<课程>/         课程介绍与各次开课页
  assets/materials/<学期>/<课程>/  对应开课的附件
templates/                       课程、开课页与日程模板
examples/                        原创示例代码源文件
scripts/                         构建资料与站点检查工具
.github/workflows/pages.yml       自动检查与发布
```

## 依赖与示例课件

`requirements.in` 记录直接依赖，`requirements.txt` 锁定已验证的完整依赖版本。日常安装使用后者，更新依赖后重新构建和检查。

PDF 与 ZIP 已包含在仓库，构建网站无需安装 PDF 工具。需要重新生成示例资料时：

```powershell
python -m pip install -r requirements-tools.txt
python scripts/build_demo_materials.py
```

PDF 使用白底版式并标注“示例”。脚本在 Windows 优先嵌入宋体，也支持通过 `--font` 指定可嵌入的中文 TrueType 字体。

## 来源与许可

网站组织参考 [清华酒井科协暑培 2026](https://summer26.net9.org/)，页面与示例资料为本项目原创编写。项目原创代码和资料采用 [MIT 许可](LICENSE)；第三方资料遵循其原有许可，上传时保留作者、来源和许可说明。
