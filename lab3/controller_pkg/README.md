# controller_pkg 控制器源码说明

## 三个主要文件

| 文件 | 通俗作用 | 改了什么 | Ubuntu位置 |
|---|---|---|---|
| [src/controller_node.cpp](src/controller_node.cpp) | 管怎么飞 | 补齐11处空白，读取状态、算误差、算推力和力矩、发4个转速 | `~/vnav_ws/src/controller_pkg/src/controller_node.cpp` |
| [src/traj_publisher.cpp](src/traj_publisher.cpp) | 管飞到哪里 | 保留给定轨迹，当前STATIC_POSE=0为绕圆 | 同包src目录 |
| [launch/traj_tracking.launch](launch/traj_tracking.launch) | 管怎么启动 | 启动两个节点，设置最终增益默认值 | 同包launch目录 |

## 其他必须保留的文件

| 文件 | 用途 |
|---|---|
| [CMakeLists.txt](CMakeLists.txt) | 告诉catkin如何构建程序 |
| [package.xml](package.xml) | ROS软件包信息和依赖 |
| [rviz/lab3.rviz](rviz/lab3.rviz) | RViz显示配置 |

## 核心实现与参数

| 项目 | 说明 |
|---|---|
| 控制主线 | 目标与实际 → 误差 → 期望力与姿态 → 力矩 → 四旋翼转速 |
| 坐标系 | ROS的z向上；按题目桥接约定将角速度从世界系转到机体系 |
| 旋翼编号 | 1在(+x,+y)，2在(-x,+y)，3在(-x,-y)，4在(+x,-y) |
| 偏航符号 | 按官方仿真器图依次为+、-、+、- |
| 转速 | 单位rad/s；仿真器支持有符号转速 |
| 默认增益 | kx=2、kv=3、kr=3、komega=1 |
| 简化项 | 省略期望角速度和角加速度前馈；没有加入D2的阻力补偿 |
| 提交范围 | 交整个controller_pkg，不能只交cpp |
| 复现 | [完整操作手册](../08_从零准备到检查演示与录制.md) |
| 返回 | [Lab3首页](../README.md) |
