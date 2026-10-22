# 安装、修复与数据采集脚本

[返回上一级](../README.md)

这里负责把实验准备好、把故障日志和运行材料保存下来。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| catkin | ROS工程使用的编译工具 |
| rosdep | 根据包清单安装系统依赖的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 补丁 | 替换原工程中一部分文件的修改 |
| 节点 | 一个正在工作的ROS程序 |
| 航点 | 希望依次经过的目标位置 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| FFmpeg | 用于命令行录制视频的工具 |
| Xorg | 支持本项目桌面录制方式的显示会话 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 安装补丁 | Lab4代码和依赖未放好 | 保留Lab3，备份后安装并构建 | 得到可继续验证的工作空间 |
| 修复缓存 | 依赖搬动后仍指向旧目录 | 补gflags_catkin、备份build/devel后重建 | 解决已报告的路径与缺包问题 |
| 采集材料 | 视频与飞行数据容易对不上 | 同轮保存视频、bag、参数和代码 | 便于复盘和计算误差 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 脚本索引 |
| [install_lab4.sh](install_lab4.sh) | 首次安装Lab4补丁，需已有工具和Lab3 |
| [repair_nlopt.sh](repair_nlopt.sh) | 修复NLopt下载失败并继续编译 |
| [repair_dependencies.sh](repair_dependencies.sh) | 修复缺gflags_catkin和旧构建缓存 |
| [find_simulator.py](find_simulator.py) | 识别场景路径，生成sim.env |
| [record_race.sh](record_race.sh) | 命令行录屏与录bag |
| [build_patch.py](build_patch.py) | 从官方模板重新生成五个补丁文件，仅供维护 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| install_lab4.sh：主流程 | 备份、去重、安装、构建 | 只复制指定的五个程序文件 |
| repair_dependencies.sh：主流程 | 补源码依赖并重建 | 不修改src内实验代码 |
| find_simulator.py：主流程 | 找到赛门CSV和可执行文件 | 只接受唯一有效场景 |
| record_race.sh：finish() | 结束录像和录包 | 等待写完，再输出保存位置 |
| build_patch.py：主流程 | 下载模板并填充Part | 会覆盖patches内五个程序文件，平时无需运行 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 已完成的Lab3、网络、Xorg桌面和正在运行的ROS节点 | Xorg是可供脚本录制桌面的显示会话 |
| 输出 | ~/lab4_evidence/backups与logs | 备份目录、txt日志 |
| 输出 | ~/lab4_evidence/sim.env | SIM_EXEC、SIM_DATA两项Shell变量 |
| 输出 | ~/lab4_evidence/runs/run_时间/ | race.mp4、race.bag、parameters.yaml、bag_info.txt、代码快照和日志 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 录屏帧率 | 每秒保存多少帧画面 | 20 |
| 准备时间 | 录屏启动前摆好窗口的时间 | 5秒；前面另有2秒录包存活检查 |
| 停止方式 | 飞行结束后正常保存 | 回录制终端按Enter |
| 重建并发 | 修复脚本控制编译资源 | -j2 -p1 |
| 日志 | 安装/修复的记录位置 | ~/lab4_evidence/logs |

## 原理通俗讲解

catkin是ROS的编译工具；build和devel保存编译产物，不是手写源码。搬动依赖后旧产物记住了错误路径，就先备份再重建。gflags_catkin是把参数处理库接入catkin的源码包。rosdep根据包内清单安装系统依赖。FFmpeg负责录桌面，rosbag负责记录消息，二者放进同一轮目录以免拿错。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 安装 | bash ~/lab4_quickstart/scripts/install_lab4.sh |
| NLopt下载修复 | bash ~/lab4_quickstart/scripts/repair_nlopt.sh |
| 依赖与缓存修复 | bash ~/lab4_quickstart/scripts/repair_dependencies.sh |
| 定位 | python3 ~/lab4_quickstart/scripts/find_simulator.py |
| 录制 | 先启跟随器，再运行record_race.sh，最后发布航点 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
