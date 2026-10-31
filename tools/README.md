# 仓库维护工具

[返回首页](../README.md) · [提交说明](../CONTRIBUTING.md)

## 检查资料链接

在仓库根目录运行：

```bash
python tools/check_navigation.py
```

默认检查当前检出的Markdown。完整克隆或想核对历史文档时，使用：

```bash
python tools/check_navigation.py --all
```

工具只读取文件与Git路径清单，不修改仓库。即使稀疏检出没有下载PDF和视频，也能判断目标路径是否在Git中。`--all`可能需要Git下载尚未检出的Markdown内容。

成功返回0，缺少路径返回1并列出来源文档和目标。检查不访问外部网站，不判断页面锚点、PDF布局或实验结论。
