# 脚本使用说明

| 脚本 | 做什么 | 什么时候运行 |
|---|---|---|
| [install_controller.sh](install_controller.sh) | 备份原包，下载3个控制文件，设为初次悬停并编译 | 第一次安装补全版控制器；已调好后不要重复运行 |
| [record_evidence.sh](record_evidence.sh) | 同时保存约40秒桌面视频、ROSbag与当前增益 | 无人机稳定绕圆后录制证据 |

| 录制要求 | 说明 |
|---|---|
| 运行环境 | Ubuntu图形桌面X11；已有ROS、ffmpeg、x11-utils |
| 运行前 | Unity、桥接和控制器保持运行，RViz先摆好视角 |
| 运行后 | 5秒内切到最大化RViz，不改桌面分辨率 |
| 保存位置 | `~/lab3_evidence`，按同一时间标签保存mp4、bag、txt |
| 首次下载与命令 | [完整演示录制手册](../08_从零准备到检查演示与录制.md) |
| 返回 | [Lab3首页](../README.md) |
