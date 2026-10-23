# 报告与个人理论交付

[返回上一级](../README.md)

集中放置可交的PDF和可编辑原稿。报告按用户提供模板组织为摘要、引言、实验设置、结果、讨论、结论和参考文献，附四个Part的核心代码及详细注释。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 说明方法和真实结果 | 集中放置可交的PDF和可编辑原稿。报告按用户提供模板组织为摘要、引言、实验设置、结果、讨论、结论和参考文献，附四个Part的核心代码及详细注释。 | 18页中文报告、18页英文报告、两题各中英文、共四份2页理论PDF及3页验收提纲 | 报告与推导可以复查和修改 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [assets](assets) | 进入下层README查看任务与逐文件清单 |
| [Lab4_助教验收讲解提纲_黄博宇.pdf](Lab4_助教验收讲解提纲_黄博宇.pdf) | 3页口头讲解：开场、演示顺序、实测数字、常见追问 |
| [build_acceptance_guide.py](build_acceptance_guide.py) | 重建验收讲解PDF；需要ReportLab与Windows微软雅黑字体 |
| [Lab4_实验报告_黄博宇.pdf](Lab4_实验报告_黄博宇.pdf) | 18页中文报告：13幅图、11张表、4个Part的代码注释 |
| [render_readable_report.py](render_readable_report.py) | 旧入口兼容包装，调用当前模板排版脚本 |
| [build_reports.py](build_reports.py) | 重建中英文报告、四份中英文理论PDF的排版源码 |
| [deliverable_1.pdf](deliverable_1.pdf) | 2页英文单段轨迹理论解答 |
| [deliverable_2.pdf](deliverable_2.pdf) | 2页英文多段约束计数理论解答 |
| [Lab4_Report_EN_Boyu_Huang.pdf](Lab4_Report_EN_Boyu_Huang.pdf) | 18页英文报告，正文与中文版本对应 |
| [Lab4_Report_EN.md](Lab4_Report_EN.md) | 可编辑英文原稿，含英文代码注释 |
| [render_template_reports.py](render_template_reports.py) | 按所给模板生成中英文PDF，支持表格、图注与代码块；需要ReportLab、Pillow和Windows字体 |
| [实验报告.md](实验报告.md) | 可编辑实验报告原稿 |
| [Deliverable_1_EN.md](Deliverable_1_EN.md) | Deliverable 1英文原稿，含各小问与结果检查 |
| [Deliverable_2_EN.md](Deliverable_2_EN.md) | Deliverable 2英文原稿，区分显式约束和自然条件 |
| [deliverable_1_CN.pdf](deliverable_1_CN.pdf) | 2页中文个人题1，与英文版公式和结论一致 |
| [deliverable_2_CN.pdf](deliverable_2_CN.pdf) | 2页中文个人题2，解释连续条件与自然条件 |
| [Deliverable_1_CN.md](Deliverable_1_CN.md) | 中文个人题1可编辑原稿 |
| [Deliverable_2_CN.md](Deliverable_2_CN.md) | 中文个人题2可编辑原稿 |
| [build_theory_deliverables.py](build_theory_deliverables.py) | 单独重建四份中英文理论PDF，不改动实验报告 |
| [理论推导.md](理论推导.md) | 可编辑的完整理论推导 |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| build_reports.py | 重建6个报告/理论PDF | 读取Markdown原稿与截图 |
| deliverable_1.pdf | 单段轨迹的全部小问 | 原端点与额外终点速度约束 |
| deliverable_2.pdf | 多段约束计数与推广 | 说明自然条件和显式约束区别 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | metrics.json、原始截图、数学推导 | 不虚构成绩 |
| 输出 | 7份PDF、7份Markdown与历史公式素材 | 18+18+2+2+2+2+3页 |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| 作者 | 已知学生信息 | 黄博宇 24020036026 |
| 日期 | 文档修订日期 | 2026年10月23日 |

## 原理通俗讲解

报告中的实测数值来自bag，理论结果来自数学求解；两者分开说明。PDF是固定版式文件，Markdown和排版脚本是可编辑来源。视频和bag直接上传作业平台，无需补充外部链接。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | 视频和bag直接上传作业平台，无需外部链接 |


## 最终报告版本

| 语言 | 唯一提交版本 | 内容确认 |
|---|---|---|
| 中文 | [Lab4_实验报告_黄博宇.pdf](Lab4_实验报告_黄博宇.pdf) | 完整流程；平均目标高度2.53m，平均低5.47cm，偏差率2.16% |
| 英文 | [Lab4_Report_EN_Boyu_Huang.pdf](Lab4_Report_EN_Boyu_Huang.pdf) | 与中文版一致；后续提速由小组共同完成 |

仓库当前目录只提供以上两份最终报告PDF；Markdown为对应可编辑原稿。
