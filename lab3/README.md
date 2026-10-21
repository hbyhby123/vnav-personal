# Lab3 无人机轨迹生成与跟踪控制

## 一眼看清这个实验

| 项目 | 内容 |
|---|---|
| 学生 | 黄博宇，24020036026，中外计科一班，第8组 |
| 实验日期 / 文档更新 | 2026年10月21日 / 2026年10月22日 |
| 实验目标 | 给无人机一个目标，控制器调整4个旋翼转速，让它先悬停、再稳定绕圆 |
| 主要编程任务 | 补全几何控制器；圆轨迹生成器由课程提供，并非自行实现路径搜索算法 |
| 实验环境 | Ubuntu20.04.6、ROS Noetic、VMware、TESSE、RViz |
| 源码与题面 | [VNAV2021源码](https://github.com/MIT-SPARK/VNAV-labs/releases/tag/VNAV2021) / [2023题面](https://vnav.mit.edu/labs_2023/lab3/exercises.html) |
| 一键下载 | **[完整交付包ZIP](archives/Lab3_完整提交材料_黄博宇.zip)** |

## 任务与交付总表

| 任务 | 要做什么 | 交付文件 | 当前状态 |
|---|---|---|---|
| D1 个人10分 | 四元数互转、标量分量、yaw、Eigen矩阵，共5问 | [deliverable_1.txt](deliverable_1.txt) | 已准备 |
| D2A 个人 | 比较两种旋翼配置的分配矩阵秩，解释控制能力 | [deliverable_2.pdf](deliverable_2.pdf)，第1页 | 已准备 |
| D2B 个人 | 推导如何用速度相关阻力补偿改善控制 | 同一PDF第2页 | 已准备；代码未加入该补偿，不声称做过补偿对比 |
| D3 团队50分 | 补齐控制器、编译、调参、跟踪圆轨迹 | [完整controller_pkg](controller_pkg/README.md) | 已完成运行与材料整理 |
| D3 视频 | 在RViz中连续完成至少一圈 | [40秒视频](evidence/circle_20261021_081755/V01_RViz_circle_20261021_081755.mp4) | 已录制并备份 |
| 视频链接文件 | 按MIT要求使用Drive/Dropbox公开视频链接 | rviz_drone_flight.txt | **待补真实链接，未生成占位文件** |
| 综合报告 | 说明原理、操作、调参、真实结果与局限 | [10页PDF](Lab3_实验报告_黄博宇.pdf) / [可编辑原稿](Lab3_实验报告_可编辑原稿.md) | 已准备 |
| 正式提交 | 个人与团队材料放到老师指定仓库 | 按当前课程要求 | 提交回执尚未确认 |

## 文件从哪里看

| 目录或文件 | 你会看到什么 | 适合什么时候看 |
|---|---|---|
| [controller_pkg](controller_pkg/README.md) | 最终完整源码，圆轨迹模式 | 看代码、交团队源码 |
| [analysis](analysis/README.md) | 真正从bag计算的轨迹、误差和逐样本CSV | 写结果分析、复算指标 |
| [screenshots](screenshots/README.md) | 8张原始截图，编号和用途 | 对照操作过程 |
| [evidence](evidence/README.md) | 原始视频、bag与实测参数 | 证明飞行结果、检查演示 |
| [scripts](scripts/README.md) | 安装与同时录屏/录包脚本 | 初次准备、再次录制 |
| [从零到检查演示](08_从零准备到检查演示与录制.md) | 从已装ROS的环境准备到完整演示命令 | 所有终端关掉后重开 |
| [复习速记](操作与复习/检查演示速记.md) | 检查时应会解释的关键点 | 检查前快速复习 |
| [archives](archives/README.md) | 打包下载版 | 离线备份、整理提交 |

## 最终参数与真实结果

| 项目 | 结果 | 怎么理解 |
|---|---|---|
| 最终增益 | kx=2，kv=3，kr=3，komega=1 | 已按实际飞行参数保存默认值 |
| 轨迹 | 半径5米、高度2米、一圈约12.57秒 | 课程提供的圆轨迹 |
| 分析区间 | ROS时间933.72—978.36秒，共44.64秒 | 不是直接拿视频时长计算 |
| 对齐位置样本 | 2233点，约3.55圈 | 使用共同时间范围全部样本 |
| 三维位置RMSE | **0.1052米，约10.52厘米** | 衡量整体位置跟踪偏差 |
| 最大三维误差 | 0.1166米 | 这段录制里的最大值 |
| 平均高度 | 1.9446米 | 比目标低约5.54厘米 |
| 平均半径 | 5.0466米 | 比目标大约4.66厘米 |
| yaw RMSE | 9.524度 | 存在偏航滞后，不能说所有误差已消除 |
| 视频 | 40秒、15fps | 已检查文件，用户确认播放正常 |
| [轨迹图](analysis/trajectory.png) / [误差图](analysis/tracking_errors.png) | 与[metrics.json](analysis/metrics.json)对应 | 指标来自真实bag，没有编造或按误差筛点 |

## 检查时怎么启动

| 顺序 | 新终端做什么 | 命令或位置 |
|---|---|---|
| 1 | 打开Unity | `cd ~/vnav-builds/lab3`，再运行`./lab3.x86_64` |
| 2 | 打开桥接 | source ROS及工作空间，再运行`roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch` |
| 3 | 打开RViz | source环境，`roscd controller_pkg`，`rviz -d rviz/lab3.rviz` |
| 4 | 启动控制器 | `roslaunch controller_pkg traj_tracking.launch kx:=2 kv:=3 kr:=3 komega:=1` |
| 切换模式 | 先停控制器，改代码再编译 | STATIC_POSE=1悬停，0绕圆；按R重置后启动 |
| 详细命令 | 不熟悉source或编译时看这里 | [完整演示手册A部分](08_从零准备到检查演示与录制.md) |

## 通俗复习表

| 问题 | 一句话回答 |
|---|---|
| 控制器到底做什么 | 比较目标与实际，算力和力矩，再算4个转速 |
| 三个话题 | desired_state是目标，current_state是实际状态，rotor_speed_cmds是转速命令 |
| 为什么先悬停 | 先把位置和姿态调稳，再增加绕圆难度 |
| 为什么一开始翻转 | 初始姿态增益过大，命令剧烈反向；降低增益后逐步稳定 |
| 为什么还会有偏航误差 | 本次按允许简化省略期望角速度前馈，持续转向时需要一定姿态误差平衡阻尼 |
| D2A为什么rank=3不行 | 滚转与偏航力矩被耦合，不能一般地独立控制位置与yaw |
| D2B补偿怎么理解 | 估计阻力，再在期望合力里抵消它；本次只做理论推导 |
| 能否直接用到真实无人机 | 不能；这是课程仿真实现，支持有符号旋翼转速 |

## 提交前最后核对

| 核对项 | 说明 |
|---|---|
| 个人材料 | deliverable_1.txt与deliverable_2.pdf放个人仓库lab3 |
| 团队材料 | 整个controller_pkg与rviz_drone_flight.txt放老师指定团队仓库lab3 |
| 视频平台 | GitHub是备份；若按MIT原要求，仍须补Drive/Dropbox公开链接 |
| 整理版参数 | 用户原包保留；此版仅统一默认值与运行参数，算法不因整理而改变 |
| 编译说明 | 用户已在Ubuntu成功编译和飞行；整理默认值后本机没有ROS，现场仍按手册catkin build |
| 原始结果 | 单次悬停高度与整段圆轨迹RMSE是不同指标，不混用 |
| 返回 | [仓库首页](../README.md) |
