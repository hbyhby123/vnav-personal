# Lab3 无人机轨迹生成与跟踪控制

**最终交付入口：[英文版提交包](submission/README.md)。仅交最新英文报告，D2为英文版；视频公开链接仍待补充。**

## 项目简介

这个实验让仿真无人机先在固定位置悬停，再沿圆轨迹飞行。控制器相当于自动驾驶员：比较目标与实际状态，持续调整四个旋翼的转速。

## 名词说明

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让多个程序通过消息协作的软件框架 |
| RViz | 查看坐标、位姿和消息状态的观察窗口 |
| TESSE | 本实验使用的无人机仿真环境 |
| catkin | ROS中编译和组织软件包的工具 |
| 四元数 | 用4个数表示三维方向的方法 |
| Eigen | C++中用于向量和矩阵计算的库 |
| 矩阵秩 | 一组关系中真正独立的关系数量 |
| 几何控制 | 直接根据机身方向计算姿态纠正动作的方法 |
| 控制分配 | 把总推力和力矩换算为各个旋翼的命令 |
| 闭环控制 | 反复比较目标与实际，再根据偏差纠正动作 |
| 力矩 | 使物体旋转或改变旋转状态的作用 |
| yaw | 机身在水平方向的转向角 |
| RMSE | 误差平方后求平均再开方，较大偏差权重更明显 |
| bag | 按时间保存ROS消息的记录文件 |
| CSV | 逗号分隔的文本表格 |
| PDF | 固定排版文档格式 |

## 任务内容

| **任务** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| D1 旋转转换 | 用正确数据类型表达方向 | 四元数是用4个数表示方向的方法；ROS接口与Eigen矩阵转换 | 完成5问文本答案 |
| D2A 控制能力 | 解释改变旋翼配置后为何失去独立控制能力 | 矩阵秩分析：比较有多少独立控制关系 | 得到rank=4与rank=3的推导 |
| D2B 阻力补偿 | 说明如何抵消速度相关阻力 | 在期望合力中减去估计外力 | 得到理论补偿方案；本次未加入飞行代码 |
| D3 控制与轨迹 | 让无人机稳定跟踪给定目标 | 几何控制：按机身方向计算纠正动作；旋翼控制分配 | 完整控制器、实际圆轨迹视频和数据 |
| 结果与复习 | 说明实际完成了什么、误差多大 | ROSbag数据对齐与统计，配套报告和演示步骤 | 可复算结果与可复习材料 |

## 交付文件清单

| **文件 / 目录** | **作用** | **说明** |
| --- | --- | --- |
| [submission/](submission/README.md) | 最终交付ZIP：英文报告、D1、D2、代码、视频 | 与桌面最终版一致 |
| [code/](code/README.md) | 最终代码和原始代码对照 | 进入下层查看逐文件清单 |
| [data/](data/README.md) | 原始记录与离线分析结果 | 进入下层查看逐文件清单 |
| [deliverables/](deliverables/README.md) | 正式报告和个人理论题 | 进入下层查看逐文件清单 |
| [review/](review/README.md) | 完整操作、复习要点与实用脚本 | 进入下层查看逐文件清单 |
| [README.md](README.md) | 本层任务、文件、输入输出、参数和原理说明 | 说明文件 |

| **实际交付文件** | **作用** | **说明** |
| --- | --- | --- |
| [英文实验报告PDF](deliverables/Lab3_Report_EN_Huang_Boyu.pdf) | 13页完善版；唯一提交报告 | 已完成 |
| [deliverables/deliverable_1.txt](deliverables/deliverable_1.txt) | 个人D1五问 | 已准备 |
| [deliverables/deliverable_2.pdf](deliverables/deliverable_2.pdf) | 个人D2英文推导 | 2页PDF |
| [完整controller_pkg](code/controller_pkg/README.md) | 团队控制器源码 | 保持整包，不只交cpp |
| [RViz视频](data/raw/circle_20261021_081755/V01_RViz_circle_20261021_081755.mp4) | 连续飞行记录 | 40秒 |
| rviz_drone_flight.txt | 填写Drive/Dropbox公开链接 | 尚待真实链接；当前没有这个文件 |

## 环境与快速开始

| **步骤** | **命令 / 操作** | **说明** |
| --- | --- | --- |
| 环境 | Ubuntu20.04.6、ROS Noetic、catkin_tools、TESSE、RViz | ROS是程序消息协作框架；RViz是观察窗口，TESSE是仿真场地 |
| 先准备 | 新环境先看[首次环境准备](review/环境准备与完整操作.md) | 本仓库不包含ROS安装包、仿真器二进制或全部外部依赖 |
| 终端1 | cd ~/vnav-builds/lab3 && ./lab3.x86_64 | 打开Unity仿真器后保持运行 |
| 终端2 | source /opt/ros/noetic/setup.bash && source ~/vnav_ws/devel/setup.bash && roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch | 桥接就是在仿真器和ROS之间传消息的翻译员 |
| 终端3 | source /opt/ros/noetic/setup.bash && source ~/vnav_ws/devel/setup.bash && roscd controller_pkg && rviz -d rviz/lab3.rviz | 观察实际与期望状态 |
| 终端4 | source /opt/ros/noetic/setup.bash && source ~/vnav_ws/devel/setup.bash && roslaunch controller_pkg traj_tracking.launch kx:=2 kv:=3 kr:=3 komega:=1 | 已有工作空间时启动控制器 |
| 切模式 | 先Ctrl+C停控制器；改STATIC_POSE；catkin build；按R重置；重启 | 1悬停、0圆轨迹；修改C++必须编译 |

## 目录结构

```text
lab3/
├── README.md                 总览、任务和快速开始
├── deliverables/             正式报告、D1、D2与可编辑原稿
│   └── assets/equations/     文稿引用的公式图
├── review/                   操作手册与复习速记
│   └── scripts/              安装和录制脚本
├── data/
│   ├── raw/                  原始视频、bag、参数与截图
│   └── analysis/             指标、CSV、图像与复算代码
└── code/
    ├── controller_pkg/       最终可运行的完整ROS包
    │   ├── src/              控制器与轨迹源程序
    │   ├── launch/           启动与参数配置
    │   └── rviz/             观察窗口配置
    └── original/             课程模板与原始上传快照
```

| **目录** | **一句话说明** |
| --- | --- |
| [deliverables](deliverables/README.md) | 交作业看这里，公式素材用于保持原稿可编辑 |
| [review](review/README.md) | 复习和演示看这里，只保留两份主说明 |
| [data](data/README.md) | 原始证据与派生分析分开保存 |
| [code](code/README.md) | 最终包与原始模板分开，运行只用controller_pkg |

## 核心原理通俗讲解

无人机想向前走，通常要先倾斜，让推力分出向前的一部分。控制器先算目标与实际差多少，再决定需要怎样倾斜、转向，最后分配成四个旋翼转速。这个不断比较再纠正的过程叫闭环控制。

| **环节** | **输入** | **作用** |
| --- | --- | --- |
| 目标生成 | 按时间计算的圆轨迹 | 告诉无人机飞到哪里、以多快速度飞 |
| 状态反馈 | 实际位置、方向和速度 | 告诉控制器目前飞成什么样 |
| 几何控制 | 目标与实际的差值 | 计算总推力与机身力矩，力矩就是使机身转动的作用 |
| 旋翼分配 | 总力和力矩 | 换成4个转速；rad/s表示每秒转过的弧度数 |

## 实测结果与边界

| **项目** | **结果** | **说明** |
| --- | --- | --- |
| 最终增益 | 2 / 3 / 3 / 1 | kx / kv / kr / komega |
| 圆轨迹 | 半径5 m、高度2 m、周期约12.57 s | 轨迹生成器由课程提供 |
| 分析时段 | 44.64 s、2233点、约3.55圈 | 使用共同时间范围全部样本 |
| 位置RMSE | 0.1052 m，约10.52 cm | RMSE是平方平均后开方，突出较大的偏差 |
| 最大位置误差 | 0.1166 m | 该录制段内最大值 |
| 平均高度 / 半径 | 1.9446 / 5.0466 m | 仍有跟踪偏差 |
| yaw RMSE | 9.524° | yaw是水平转向角，存在持续转向时的滞后 |
| 正式链接 | Drive/Dropbox公开链接仍待补 | 不以GitHub备份冒充题面指定交付 |

## 交付与归档状态

| **项目** | **状态** |
| --- | --- |
| 学生 | 黄博宇，24020036026，中外计科一班，第8组 |
| 实验 / 文档日期 | 2026年10月21日 / 2026年10月22日 |
| 个人与团队提交 | 按老师指定位置分别提交；本仓库不等于正式提交回执 |
| 代码边界 | 已实际运行；省略期望角速度前馈，未做阻力补偿对比实验 |
| [仓库总览](../README.md) | 查看Lab1、Lab2与Lab3入口 |
