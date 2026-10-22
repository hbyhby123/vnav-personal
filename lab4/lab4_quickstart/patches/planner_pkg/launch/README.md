# 首门与航点启动配置

[返回上一级](../README.md)

两个launch分别用于首门验证和完整竞速前的赛门发布。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| 航点 | 希望依次经过的目标位置 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 静态测试 | 同时接好目标、控制器和赛门 | static_point_test.launch | 启动首门悬停链路 |
| 发布整组赛门 | 给竞速节点提供路线输入 | traj_gen.launch | 触发轨迹生成 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 启动顺序和参数 |
| [static_point_test.launch](static_point_test.launch) | 启动controller_node、traj_vertices_publisher、simple_traj_planner |
| [traj_gen.launch](traj_gen.launch) | 只启动traj_vertices_publisher |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| static_point_test.launch | 启动悬停相关节点 | 用于Part0，竞速前先停止 |
| traj_gen.launch | 启动赛门发布节点 | 必须等跟随器与记录器准备好再启动 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | simulator_data_directory | 场景_Data目录，里面有StreamingAssets/赛门CSV |
| 输入 | 控制器增益 | 仅static_point_test.launch设置 |
| 输出 | 运行节点和/desired_traj_vertices消息 | 航点由官方节点读取和发布 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| simulator_data_directory | 实际场景路径；两文件共有 | $(env HOME)/vnav-builds/vnav-2021-lab4/vnav-2021-lab4_Data |
| kx / kv | 位置和速度误差的反馈强度 | 2 / 3 |
| kr / komega | 朝向和转动速度的反馈强度 | 3 / 1 |

## 原理通俗讲解

launch像开机清单：告诉ROS开哪些程序、把哪些参数交给它们。赛门数据路径应来自路径识别脚本，不能照抄错误的解压目录。static_point_test会启动控制器，因此它与竞速跟随启动文件不能同时运行。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 悬停 | roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" |
| 竞速触发 | roslaunch planner_pkg traj_gen.launch simulator_data_directory:="$SIM_DATA" |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
