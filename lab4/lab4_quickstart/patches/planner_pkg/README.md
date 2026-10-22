# planner_pkg：赛门输入与首门测试

[返回上一级](../README.md)

先把第一道赛门变成悬停目标，用简单任务检查控制链路。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 补丁 | 替换原工程中一部分文件的修改 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| 位姿 | 位置加朝向 |
| 航点 | 希望依次经过的目标位置 |
| PoseArray | 一组位置和朝向 |
| MultiDOFJointTrajectoryPoint | 一个时刻的期望位置、朝向、速度和加速度消息 |
| TF | 描述两个坐标系相对位置和朝向的消息 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 第一门悬停 | 先验证位置和朝向传递正确 | Part0读取首个Pose并发布目标 | 在第一门附近保持，待实测 |
| 赛门发布配置 | 让原工程能读取正确赛道 | launch传入模拟器数据目录 | 得到按顺序排列的赛门消息 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 模块介绍 |
| [src/simple_traj_planner.cpp](src/simple_traj_planner.cpp) | Part0完整源文件 |
| [src/README.md](src/README.md) | 函数与消息解释 |
| [launch/static_point_test.launch](launch/static_point_test.launch) | 启动控制器、官方航点节点和悬停节点 |
| [launch/traj_gen.launch](launch/traj_gen.launch) | 仅启动官方航点发布节点 |
| [launch/README.md](launch/README.md) | 命令与参数说明 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| trajCB() | 生成首门期望状态 | 设置位置和姿态，速度与加速度为0 |
| main() | 注册消息收发 | 收到赛门后处理 |
| traj_vertices_publisher | 从CSV读赛门的官方节点 | 源码不在本补丁，安装时从官方工程取得 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | /desired_traj_vertices | geometry_msgs/PoseArray |
| 输出 | /desired_state | trajectory_msgs/MultiDOFJointTrajectoryPoint |
| 输出 | world → desired_pose | TF；TF是描述两个坐标系相对位置和朝向的消息 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| simulator_data_directory | 赛道数据目录 | $(env HOME)/vnav-builds/vnav-2021-lab4/vnav-2021-lab4_Data |
| kx / kv / kr / komega | 位置、速度、姿态、角速度反馈增益 | 2 / 3 / 3 / 1 |

## 原理通俗讲解

位姿就是位置加朝向。首门测试只取消息里的第一道门，把它当作固定目标，不做整条路线优化。零速度、零加速度表示到达后希望停住。悬停通过后才切换到竞速，便于判断问题来自控制器还是轨迹。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 测试 | roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" |
| 结束 | 在该终端按Ctrl+C，再启动竞速跟随器 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
