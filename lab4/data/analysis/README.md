# 轨迹与误差复算

[返回上一级](../README.md)

从原bag计算真实跟踪误差并复核理论题。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 得到可复算指标 | 从原bag计算真实跟踪误差并复核理论题。 | 时间对齐、线性插值、逐点误差与精确有理数QP | JSON、CSV、图表和理论核验结果 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [axis_rmse_comparison.png](axis_rmse_comparison.png) | 从既有metrics绘制各轴RMSE柱状图，单位cm |
| [build_axis_comparison.py](build_axis_comparison.py) | 生成各轴误差对比图，未新增测量数据 |
| [aligned_states.csv](aligned_states.csv) | 实际与期望对齐后的逐点数据 |
| [analyze_run.py](analyze_run.py) | 从bag复算统计与四幅图 |
| [desired_states.csv](desired_states.csv) | 期望状态与time_from_start原始提取 |
| [metrics.json](metrics.json) | 本轮统计指标与方法边界 |
| [position_tracking.png](position_tracking.png) | 分析图或排版公式图片，非新增实测 |
| [requirements.txt](requirements.txt) | 离线复算所需Python依赖 |
| [theory_verification.json](theory_verification.json) | 理论精确解的机器可读结果 |
| [tracking_error.png](tracking_error.png) | 分析图或排版公式图片，非新增实测 |
| [trajectory_3d.png](trajectory_3d.png) | 分析图或排版公式图片，非新增实测 |
| [trajectory_xy.png](trajectory_xy.png) | 分析图或排版公式图片，非新增实测 |
| [verify_theory.py](verify_theory.py) | 精确求解理论QP并核验约束计数 |
| [waypoint_center_distances.csv](waypoint_center_distances.csv) | 顺序局部窗口内距赛门中心最近距离；不是穿门裁判 |
| [waypoints.csv](waypoints.csv) | 12个赛门的中心位置和yaw |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| analyze() | 读取bag、对齐并输出 | 主误差窗口排除终点保持 |
| summarize() | 统计RMSE、均值、分位数和最大值 | 所有值有明确单位 |
| yaw() | 从四元数提取水平角 | 插值前先展开目标角度 |
| verify_theory.py | 精确KKT及计数恒等式 | 独立于实测飞行 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | ../raw/run_20261022_000059/race.bag | ROS1 bag |
| 输出 | metrics.json、3个状态/航点CSV与中心距离CSV | 四幅轨迹PNG、1幅RMSE对比图及理论JSON |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| 对齐基准 | bag记录时间 | 线性插值到实际状态时刻 |
| 主窗口 | 参考轨迹执行段 | 约134.17s、6708点 |
| 执行段RMSE | 3D位置 | 0.056426m |
| 最大误差 | 3D位置 | 0.084428m |

## 原理通俗讲解

RMSE是误差平方后求平均再开方。先将期望消息插值到实际消息时刻，只统计目标轨迹正在执行的窗口；不把结束后的长时间保持混在主要结果里。赛门中心距离是诊断，不是碰撞或通过检测。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | Drive/Dropbox公开视频与bag链接尚待本人提供 |
