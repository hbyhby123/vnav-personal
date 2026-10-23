# 安装 修复与录制脚本

[返回上一级](../README.md)

准备工作空间并把同轮材料保存下来。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 降低重复操作出错 | 准备工作空间并把同轮材料保存下来。 | 备份安装、依赖修复、路径识别、同时录屏与录bag | 可重跑且有日志 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [find_simulator.py](find_simulator.py) | 定位场景与CSV，生成sim.env |
| [install_lab4.sh](install_lab4.sh) | 备份并安装归档的3个完整ROS包，已有依赖时使用 |
| [record_race.sh](record_race.sh) | 同时录像、录消息并保存参数与关键代码 |
| [repair_dependencies.sh](repair_dependencies.sh) | 修复gflags_catkin及旧编译路径缓存 |
| [repair_nlopt.sh](repair_nlopt.sh) | 下载并校验NLopt原始归档，再继续构建 |
| [setup_dependencies.sh](setup_dependencies.sh) | 安装外部依赖与bridge，处理重复包与NLopt下载 |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| install_lab4.sh | 恢复完整三包并编译 | 需已有依赖，自动备份原包 |
| setup_dependencies.sh | 安装依赖与bridge | 新工作空间需先复制归档包 |
| repair_dependencies.sh | 修复缺包与旧路径缓存 | 备份旧编译产物 |
| repair_nlopt.sh | 从直连下载NLopt并校验 | 使用本地归档继续构建 |
| find_simulator.py | 找到唯一有效场景 | 生成SIM_EXEC和SIM_DATA |
| record_race.sh：finish() | 结束录像和bag并等待落盘 | 通关后按Enter |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | Ubuntu20.04/Noetic、网络、桌面和节点 | ROS本体不由这些脚本安装 |
| 输出 | ~/vnav_ws和~/lab4_evidence | 源码、日志、视频与bag |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| 录屏帧率 | 每秒录像帧数 | 20 |
| 准备时间 | 开始录屏前等待 | 5秒 |
| 结束方式 | 正常保存 | 按Enter，不直接关虚拟机 |

## 原理通俗讲解

安装脚本只恢复归档程序，依赖脚本才准备外部库。FFmpeg录桌面，rosbag录消息。Xorg是本录屏方式需要的桌面会话。不要在没有目标发布者时启动录制。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | 视频和bag直接上传作业平台，无需外部链接 |
