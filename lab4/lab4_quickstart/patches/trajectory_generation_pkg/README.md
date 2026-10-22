# trajectory_generation：轨迹生成与跟随

[返回上一级](../README.md)

把赛门连接成平滑轨迹，再逐时刻把目标交给Lab3控制器。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| PoseArray | 一组位置和朝向 |
| Odometry | 包含实际位置、朝向和速度的状态消息 |
| MultiDOFJointTrajectoryPoint | 一个时刻的期望位置、朝向、速度和加速度消息 |
| yaw | 从上往下看时无人机面向的角度 |
| snap | 位置的四阶导数；最小化它用于抑制猛烈的轨迹变化 |
| bag | 记录ROS消息的原始数据文件 |
| time_scale | 把估计飞行时间乘一个倍率；数值大时分配的时间更长 |
| Hz | 每秒发生多少次；50Hz就是每秒50次 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 状态读取 | 避免从错误或未初始化位置出发 | Part1.1读取当前状态 | 起点有效 |
| 轨迹优化 | 按顺序经过赛门且朝向连续 | Part1.2分别优化位置与yaw | 得到位置和朝向随时间变化的曲线 |
| 目标发布 | 让控制器持续获得新的目标 | Part1.3按经过时间采样 | 实际飞行可跟随，待验证 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 模块总览 |
| [src/trajectory_generation_node.cpp](src/trajectory_generation_node.cpp) | Part1.1、1.2、1.3 |
| [src/README.md](src/README.md) | 函数、时间和消息说明 |
| [launch/traj_following.launch](launch/traj_following.launch) | 启动轨迹节点及控制器 |
| [launch/README.md](launch/README.md) | 参数和启动说明 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| onCurrentState() | 更新实际位置和朝向 | 收到有效状态才允许规划 |
| generateOptimizedTrajectory() | 连接赛门并优化 | 分别计算三维位置和单维朝向 |
| publishDesiredState() | 采样并发布目标 | 时间超过终点后使用末端状态 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | /current_state | nav_msgs/Odometry |
| 输入 | /desired_traj_vertices | geometry_msgs/PoseArray |
| 输出 | /desired_state | trajectory_msgs/MultiDOFJointTrajectoryPoint |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| ROS包名 | roslaunch使用的名字 | trajectory_generation，区别于文件夹名 |
| time_scale | 段时间倍率 | 2.0，低于1或非有限值时重设为1 |
| 发布频率 | 每秒发多少个目标 | 50Hz |

## 原理通俗讲解

yaw就是从上往下看无人机面向的角度。先让位置经过所有门，再把yaw在±π交界处展开，避免突然转一整圈。优化器最小化snap，也就是位置的四阶导数；可以理解为抑制轨迹变化过于猛烈的一种平滑目标。它不自动保证避障或穿门成功，仍需看实际视频和数据。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 启动 | roslaunch trajectory_generation traj_following.launch time_scale:=2.0 |
| 触发 | 记录器准备好后再运行planner_pkg traj_gen.launch |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
