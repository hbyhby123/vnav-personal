#!/usr/bin/env python3
"""检查Markdown中的仓库内相对链接，只读文件，不修改材料。

默认检查当前检出的Markdown。--all检查Git已经跟踪的全部Markdown；
稀疏检出时，从Git读取尚未下载的文档内容，但不要求下载视频或报告。
"""
import argparse
import os
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "__pycache__", "node_modules", ".report_packages",
        "build", "devel", "install"}


def git_output(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def local_files():
    # 跳过工具缓存和构建目录，只收集文件名，不读取大型媒体内容。
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [name for name in dirs if name not in SKIP]
        for name in files:
            yield (Path(folder) / name).relative_to(ROOT).as_posix()


def target_path(document, target):
    """返回规范化后的仓库路径；外部URL和本页锚点返回None。"""
    target = target.strip().strip("<>")
    if not target or target.startswith("#") or urlsplit(target).scheme:
        return None
    target = unquote(urlsplit(target).path)
    if not target:
        return None
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(document), target))


def check(all_tracked=False):
    # Git树提供完整路径清单，即使当前使用稀疏检出也能识别有效目标。
    tracked = set(git_output("ls-tree", "-r", "--name-only", "HEAD").decode().splitlines())
    working = set(local_files())
    available = tracked | working
    for path in list(available):
        parent = posixpath.dirname(path)
        while parent:
            available.add(parent)
            parent = posixpath.dirname(parent)
    documents = sorted(path for path in (tracked if all_tracked else working)
                       if path.endswith(".md"))
    missing = []
    count = 0
    for document in documents:
        file = ROOT / document
        if file.exists():
            text = file.read_text(encoding="utf-8-sig")
        else:
            text = git_output("show", "HEAD:" + document).decode("utf-8-sig")
        # 示例代码里的占位链接不属于导航，先移除代码块。
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for raw in re.findall(r"\]\(([^)]+)\)", text):
            target = target_path(document, raw)
            if target is None:
                continue
            count += 1
            if target not in available:
                missing.append((document, raw, target))
    return documents, count, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="检查全部已跟踪Markdown")
    args = parser.parse_args()
    documents, count, missing = check(args.all)
    print(f"检查了{len(documents)}份Markdown、{count}个仓库内链接。")
    for document, raw, resolved in missing:
        print(f"缺失：{document} -> {raw}（解析为{resolved}）")
    if missing:
        print(f"共{len(missing)}处需要核对。")
        return 1
    print("未发现缺失路径。外部网站、页面锚点和实验结论不在此检查范围。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
