# 轨迹优化与目标跟随 源码与函数

[返回上一级](../README.md)

保存本包实际编译的源程序。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 按时间生成飞行目标 | 保存本包实际编译的源程序。 | 位置与yaw分开优化，最小snap | 完整赛道参考轨迹及跟随 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [spiral_pose_publisher.cpp](spiral_pose_publisher.cpp) | 原工程附带的螺旋目标程序，非本轮启动主线 |
| [trajectory_generation_node.cpp](trajectory_generation_node.cpp) | Part1.1～1.3轨迹规划与采样发布 |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| onCurrentState() | 更新位置和朝向 | 等待有效起点 |
| generateOptimizedTrajectory() | 添加顶点约束并求解 | 末端按库设置边界 |
| publishDesiredState() | 按经过时间采样并发布 | 越过总时长后保持末端 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | /current_state、/desired_traj_vertices | Odometry、PoseArray |
| 输出 | /desired_state | MultiDOFJointTrajectoryPoint |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| 实际包名 | roslaunch使用的名字 | trajectory_generation |
| D / N | 维度 / 系数数目 | 3 / 10，最高九次 |
| v_max / a_max | 估计段时间用的参数 | 8 / 4，不是硬上限 |
| time_scale / 发布频率 | 时间倍率 / 每秒发布次数 | 2.0 / 50Hz |

## 原理通俗讲解

航点是希望经过的位置。snap是位置四阶导数，最小化它用来减小目标变化的剧烈程度；它不等于自动避障或最短时间。yaw先连续展开，再与位置使用相同段时间。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | 视频和bag直接上传作业平台，无需外部链接 |
