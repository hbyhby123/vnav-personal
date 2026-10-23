# 赛门读取与首门悬停 源码与函数

[返回上一级](../README.md)

保存本包实际编译的源程序。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 建立可检查的赛门输入 | 保存本包实际编译的源程序。 | CSV解析、坐标转换、目标消息 | 首门稳定与有序赛门发布 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [simple_traj_planner.cpp](simple_traj_planner.cpp) | Part0首门悬停与目标TF |
| [traj_planner.cpp](traj_planner.cpp) | 原工程空入口，不在当前CMake构建主线中 |
| [traj_vertices_publisher.cpp](traj_vertices_publisher.cpp) | 读取CSV、转换坐标、排序并发布赛门 |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| unity2RosPose() | 转换坐标表示 | 交换位置轴并转换四元数方向 |
| load_pose_array_from_simulator() | 读表、筛选并排序门 | 返回PoseArray |
| trajCB() | 发布首门固定目标 | 零速度、零加速度及TF |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 场景_Data/StreamingAssets中的静态CSV | vnav-2020-lab4_static_tfs.csv |
| 输出 | /desired_traj_vertices、/desired_state | 赛门PoseArray、首门期望点 |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| simulator_data_directory | 实际场景目录 | 默认旧目录，启动时用SIM_DATA覆盖 |
| 首门增益 | 本轮设置 | 2/3/3/1 |

## 原理通俗讲解

CSV是表格文本；位姿是位置加朝向。原节点转换Unity与ROS坐标并排序门编号，Part0取第一门作为固定目标。它不负责整条轨迹优化。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | 视频和bag直接上传作业平台，无需外部链接 |
