"""Generate the original, clearly labelled demo slides and practice ZIP."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs/assets/materials/2026-fall/git"
WIDTH, HEIGHT = 960, 540


def make_pdf(path: Path, font_path: Path | None):
    if font_path is None and os.name == "nt":
        candidate = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/simsun.ttc"
        if candidate.is_file():
            font_path = candidate
    if font_path is not None:
        pdfmetrics.registerFont(TTFont("CourseChinese", str(font_path), subfontIndex=0))
        font = "CourseChinese"
    else:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        font = "STSong-Light"

    doc = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT), invariant=1)
    doc.setTitle("Git 与开源协作 - 原创示例课件")
    doc.setAuthor("开源安全精品课程")
    doc.setSubject("网站演示资料，不代表已确定的线下课程")
    body = ParagraphStyle("body", fontName=font, fontSize=21, leading=32, textColor=colors.HexColor("#333333"), wordWrap="CJK")

    def text(value, x, top, width=860, size=21):
        style = ParagraphStyle("item", parent=body, fontSize=size, leading=size * 1.5)
        paragraph = Paragraph(value, style)
        _, height = paragraph.wrap(width, HEIGHT)
        if top - height < 55:
            raise ValueError("Slide text overlaps the footer")
        paragraph.drawOn(doc, x, top - height)

    def page(title, number):
        doc.setFillColor(colors.white)
        doc.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
        text("网安科协 / 开源安全精品课程 / 示例课件", 48, 508, size=13)
        text(title, 48, 452, size=32)
        doc.setStrokeColor(colors.HexColor("#dddddd"))
        doc.line(48, 382, WIDTH - 48, 382)
        doc.line(48, 45, WIDTH - 48, 45)
        doc.setFillColor(colors.HexColor("#666666"))
        doc.setFont(font, 10)
        doc.drawString(48, 23, "原创示例资料 · 正式讲师、时间和地点待公布")
        doc.setFillColor(colors.HexColor("#666666"))
        doc.setFont("Helvetica", 10)
        doc.drawRightString(WIDTH - 48, 22, f"{number} / 4")

    page("Git 与开源协作", 1)
    text("学习目标", 48, 347, size=24)
    text("1. 分清工作目录、暂存区与提交记录。", 48, 298)
    text("2. 在独立练习目录中保存修改、创建分支。", 48, 246)
    text("3. 理解 Pull Request 如何帮助多人审核与协作。", 48, 194)
    text("先修：基本文件操作与终端使用。设备：笔记本电脑。", 48, 110, size=17)
    doc.showPage()

    page("从修改文件到保存一个版本", 2)
    for top, title, detail in [
        (347, "工作目录", "正在编辑的文件。使用 git diff 查看尚未暂存的修改。"),
        (252, "暂存区", "下一次提交将保存的修改。使用 git diff --staged 检查。"),
        (157, "提交记录", "已保存的项目版本。使用 git log --oneline 查看。"),
    ]:
        text(title, 48, top, size=23)
        text(detail, 48, top - 40, size=18)
    doc.showPage()

    page("在独立练习目录中保存第一次提交", 3)
    text("解压练习包，在该文件夹中打开终端。署名配置仅作用于练习仓库。", 48, 347, size=17)
    doc.setFont("Courier", 18)
    doc.setFillColor(colors.HexColor("#222222"))
    commands = [
        "git init -b main",
        'git config user.name "Your Name"',
        'git config user.email "you@example.com"',
        "git add README.md hello.py .gitignore",
        "git diff --staged",
        'git commit -m "Add practice project"',
        "git log --oneline",
    ]
    for index, command in enumerate(commands):
        doc.drawString(48, 279 - index * 27, command)
    text("运行前请将 Your Name 与邮箱替换为自己希望公开的提交署名。", 48, 77, size=14)
    doc.showPage()

    page("用一次小改动练习分支与协作", 4)
    text("创建分支，编辑 README 中的学习目标，再暂存并提交修改。", 48, 347, size=19)
    doc.setFont("Courier", 18)
    for index, command in enumerate([
        "git switch -c docs/learning-goal",
        "git add README.md",
        'git commit -m "Document my learning goal"',
        "git switch main",
        "git merge docs/learning-goal",
    ]):
        doc.drawString(48, 282 - index * 27, command)
    text("练习：说明暂存与提交的区别，并写一段项目使用说明。", 48, 124, size=17)
    text("参考：Git 官方文档 https://git-scm.com/doc · GitHub Hello World 官方教程", 48, 76, size=12)
    doc.showPage()
    doc.save()
    print(f"Created {path.relative_to(ROOT)} (4 pages; font: {font})")


def make_zip(path: Path):
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name in ["README.md", "hello.py", ".gitignore"]:
            entry = ZipInfo(f"git-collaboration-demo/{name}", date_time=(2026, 10, 2, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, (ROOT / "examples/git-collaboration" / name).read_bytes())
    print(f"Created {path.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, help="Embeddable Chinese TrueType font or TTC")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    make_pdf(OUTPUT / "git-collaboration-demo.pdf", args.font)
    make_zip(OUTPUT / "git-collaboration-demo.zip")
