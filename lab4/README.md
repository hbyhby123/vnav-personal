# Lab4 无人机控制与竞速

## 项目简介

本实验把赛门位置连接成平滑飞行轨迹，再由Lab3控制器驱动仿真无人机跟随。已归档首门悬停和一次完整通关的真实代码、截图、视频、bag与离线分析，以及报告和两道个人理论题。

## 名词说明

| **术语** | **大白话解释** |
| --- | --- |
| ROS / 节点 / 话题 | 让程序协作的框架 / 一个工作程序 / 程序交换消息的通道 |
| TESSE Unity | 本实验无人机和赛道的仿真环境 |
| catkin / rosdep | 编译ROS工程的工具 / 按清单准备依赖的工具 |
| 位姿 / 航点 | 位置加朝向 / 希望经过的目标位置 |
| yaw / 四元数 | 水平朝向角 / 用4个数表示三维方向的方法 |
| snap / QP | 位置四阶导数，用于衡量猛烈变化 / 带约束的二次代价优化 |
| 闭环 / 增益 | 反复比较目标和实际再纠正 / 反馈修正的强度 |
| bag / CSV / YAML | ROS消息记录 / 表格文本 / 参数文本 |
| RMSE | 误差平方求平均再开方，较大的偏差权重更高 |
| SHA256 | 文件内容指纹，用来验证是否逐字节一致 |
| 稀疏检出 | 只下载仓库指定目录，避免下载大视频 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| D1 单段轨迹优化，20分 | 不同次数与端点约束下如何最小化代价 | QP矩阵、有理数精确求解、约束代回 | 完整推导PDF，已生成 |
| D2 多段轨迹优化，15分 | 轨迹需要多少系数和连接条件 | Euler-Lagrange变分方程、连续与自然条件计数 | r=4与一般r阶推导PDF，已生成 |
| Part0 首门悬停 | 验证目标、坐标和控制器 | 第一门固定目标、零速度加速度、TF坐标关系 | 首门稳定，实测截图已回传 |
| Part1.1～1.3 竞速，团队65分含Part0 | 依次经过全部赛门 | 有效起点、轨迹优化、yaw展开、时间采样 | 用户确认一次完整通关，视频和bag已归档 |
| 数据与复习 | 说明真实误差并支持后期演示 | 状态时间对齐、CSV与图表、操作与问答 | 可复算指标与逐终端操作 |
| 可选加速 | 对比更短的有效通关时间 | 本次未做多轮时间倍率对比 | 不申报最快团队或额外加速成绩 |

## 交付文件清单

| **文件 / 目录** | **作用** | **说明** |
| --- | --- | --- |
| [code/](code/README.md) | 三个完整实际运行ROS包与官方模板对照 | 每层README列出文件、函数、接口和参数 |
| [data/](data/README.md) | 原始证据与可复算分析 | raw保原件，analysis存派生结果 |
| [deliverables/](deliverables/README.md) | 正式报告、个人题与可编辑原稿 | 7份PDF及重建源码 |
| [review/](review/README.md) | 操作、复习和脚本 | 只保留两份主说明，避免多份过时教程 |
| [rviz_drone_race.txt](rviz_drone_race.txt) | 真实GitHub媒体入口和正式平台链接状态 | Drive/Dropbox尚待补；不伪造公开链接 |
| [README.md](README.md) | 本层总览 | 任务、交付、运行、结果和原理 |
| [.gitignore](.gitignore) | 忽略本机分析缓存与还原视频副本 | 防止重复加入超过100MB的原视频 |
| [.gitattributes](.gitattributes) | 标记二进制与Shell换行 | 避免二进制差异噪声，Shell保持LF |

| **直接交付入口** | **内容** | **状态** |
| --- | --- | --- |
| [助教验收讲解PDF](deliverables/Lab4_助教验收讲解提纲_黄博宇.pdf) | 3页，开场介绍、演示顺序、实测结果、常见问答 | 可直接照着讲解 |
| [English report](deliverables/Lab4_Report_EN_Boyu_Huang.pdf) | 18页英文版，与中文版数据和结论一致 | 按所给模板组织，含代码注释 |
| [实验报告PDF](deliverables/Lab4_实验报告_黄博宇.pdf) | 18页中文版，含核心代码注释、13幅图与11张表 | 已生成并检查全部页面 |
| [D1中文理论PDF](deliverables/deliverable_1_CN.pdf) | 2页，单段轨迹优化中文解释 | 与英文版结果一致 |
| [D2中文理论PDF](deliverables/deliverable_2_CN.pdf) | 2页，多段轨迹连接与计数 | 与英文版条件一致 |
| [D1理论PDF](deliverables/deliverable_1.pdf) | 英文2页，单段轨迹全部小问 | 已精确核验 |
| [D2理论PDF](deliverables/deliverable_2.pdf) | 英文2页，约束计数与r阶推广 | 假设与自然条件明确 |
| [完整运行视频预览](data/raw/run_20261022_000059/race_preview.mp4) | 160.75秒，约10.8MB | 连续缩放重编码，不剪辑、不加速 |
| [原视频分片与还原](data/raw/run_20261022_000059/original_video/README.md) | 149508837字节原视频，3片 | 可恢复原视频并校验SHA256 |
| [原始bag](data/raw/run_20261022_000059/race.bag) | 原样保存5个话题 | 两个必需状态话题均非零 |
| [8张原图](data/raw/screenshots/README.md) | 连续编号01至08 | 内容与数字未修改 |
| [指标与复算](data/analysis/README.md) | JSON、CSV、4幅图与脚本 | 可从原bag独立复算 |
| [操作与演示](review/操作与演示.md) | 新环境准备与所有程序关闭后的完整启动 | 当前已有环境按[现场演示](review/操作与演示.md)操作 |
| [复习速记](review/复习速记.md) | 文件角色、算法主线、参数、结果与理论要点 | 检查前快速阅读 |

## 环境与快速开始

| **步骤** | **命令 / 操作** | **说明** |
| --- | --- | --- |
| 运行环境 | Ubuntu20.04.6、ROS Noetic、VNAV2021、TESSE Lab4 | 仿真器和ROS本体不在仓库中 |
| 新环境 | 将三个代码包放入工作空间后运行review/scripts/setup_dependencies.sh | 只取code和review；先复制三包再配依赖 |
| 终端1 | source ~/lab4_evidence/sim.env；cd "$(dirname "$SIM_EXEC")"；"$SIM_EXEC" | 分三条执行；打开Unity后按R复位 |
| 终端2 | source /opt/ros/noetic/setup.bash；source ~/vnav_ws/devel/setup.bash；roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch | 分三条执行，桥接连接仿真和ROS |
| 首门测试 | roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" | 新终端先source工作空间与sim.env；成功后Ctrl+C停止 |
| 终端3 跟随 | roslaunch trajectory_generation traj_following.launch kx:=2 kv:=3 kr:=3 komega:=1 time_scale:=2.0 | 不同时运行Lab3旧traj_tracking.launch |
| 终端4 记录 | bash ~/vnav_lab4_source/lab4/review/scripts/record_race.sh | 脚本路径按实际下载位置替换，等待记录就绪 |
| 终端5 航点 | roslaunch planner_pkg traj_gen.launch simulator_data_directory:="$SIM_DATA" | 新终端先source；最后执行以触发飞行 |
| 结束 | 通过最后一门后等3秒，回录制终端按Enter | 检查视频完整、bag话题齐全 |
| 再来一轮 | 停航点→停跟随器→Unity按R→跟随→记录→航点 | 只按R不会清除旧轨迹 |

已经完成实验时不需要重装。上表用于回顾；逐终端可直接复制的完整命令在[操作与演示](review/操作与演示.md)。

## 目录结构

```text
lab4/
├── README.md                     总览与真实状态
├── rviz_drone_race.txt            视频与bag入口，标记正式平台链接待补
├── code/
│   ├── controller_pkg/            实际运行的Lab3控制器完整包
│   ├── planner_pkg/               赛门读取与首门悬停完整包
│   ├── trajectory_generation_pkg/ 轨迹规划与跟随完整包
│   └── original/                  官方VNAV2021模板与来源指纹
├── data/
│   ├── raw/
│   │   ├── screenshots/          原始8张截图
│   │   ├── upload_manifest.json   上传tar及全部成员的SHA256
│   │   └── run_20261022_000059/    bag、参数、日志、代码快照和视频预览
│   │       └── original_video/    3个原视频分片与还原脚本
│   └── analysis/                  CSV、指标、4幅图和复算脚本
├── deliverables/                  中英报告、两份理论PDF、验收提纲与重建脚本
│   └── assets/equations/          可重建的公式图
└── review/                        操作与演示、复习速记
    └── scripts/                   安装、依赖修复、场景识别与录制
```

| **目录** | **一句话说明** |
| --- | --- |
| code | 查看实际怎么实现、怎么构建 |
| data/raw | 查看原始证据，不把分析图冒充截图 |
| data/analysis | 查看误差如何算出，能重新生成结果 |
| deliverables | 交报告与个人理论题时看这里 |
| review | 下次复习和现场演示时看这里 |

## 核心原理通俗讲解

赛门告诉无人机“应该经过哪里”，轨迹优化器把这些点连成平滑的时间曲线。程序每秒取50个目标位置、速度、加速度和朝向，交给Lab3控制器；控制器比较实际状态，再调整四个旋翼，这就是闭环跟踪。

| **环节** | **本次实现** | **复习时注意** |
| --- | --- | --- |
| 起点 | 等收到有效当前位置和yaw | 不用未初始化值规划 |
| 位置与方向 | 位置3维、yaw1维，使用相同段时间 | yaw跨±π需要连续展开 |
| 平滑 | 最小snap，端点采用库的边界设置 | 不等于自动避障或速度硬限幅 |
| 时间 | 段时间估计后乘2.0，按经过时间采样 | N=10是10个系数，最高九次 |
| 末端 | 超过总时长后使用末端状态 | 重跑需重启跟随器 |
| 核验 | 视频、同轮bag、参数、代码相互对应 | 单张终点图和中心距离不单独证明完整通关 |

## 实测结果与统计边界

| **指标** | **结果** | **统计口径** |
| --- | --- | --- |
| 完整运行 | 1轮，12个赛门位姿 | 用户确认通关，连续视频与轨迹相互核对 |
| 参数 | kx/kv/kr/komega=2/3/3/1，time_scale=2.0 | 原始parameters.yaml |
| bag总时长 | 167.28s | 含准备、飞行和末端保持 |
| 参考轨迹时长 | 134.17s | time_from_start终值，不是独立裁判成绩 |
| 执行段样本 | 6708点 | 目标时间正在推进的区间 |
| 三维位置RMSE | 0.0564m，约5.64cm | 期望状态按bag时间线性插值到实际状态时刻 |
| 最大位置误差 | 0.0844m，约8.44cm | 同一执行段 |
| X/Y/Z RMSE | 0.0072 / 0.0064 / 0.0556m | 主要偏差来自高度方向 |
| yaw RMSE | 2.292° | 先展开目标yaw，再按最短角差计算 |
| 加速比较 | — | 没有多轮成绩或最快团队比较 |

![期望与实际水平轨迹](data/analysis/trajectory_xy.png)

## 提交与来源

| **项目** | **说明** |
| --- | --- |
| 学生 | 黄博宇，24020036026，中外计科一班，第8组 |
| 文档日期 | 2026年10月22日；运行目录与原机器时间字符串保持不变 |
| 个人与团队提交 | 按老师要求分别提交；GitHub归档不等于正式提交回执 |
| 正式媒体链接 | Drive/Dropbox公开视频与bag链接仍待本人提供，rviz_drone_race.txt已真实标记 |
| 原视频 | 分片保存只是解决单文件大小，不损失原始字节；预览是额外派生文件 |
| 课程要求 | [MIT Lab4题面](https://vnav.mit.edu/labs_2023/lab4/exercises.html) |
| 代码基线 | [VNAV2021](https://github.com/MIT-SPARK/VNAV-labs/tree/VNAV2021/lab4) |
| 辅助说明 | 理论、代码准备、分析与整理使用AI辅助；运行、视频和截图来自用户Ubuntu |
| [返回仓库总览](../README.md) | 查看Lab1至Lab4入口 |
