# LAB4 无人机控制与竞速：代码补丁、操作与复习

## 项目简介

本项目把赛门位置连成平滑路线，再交给已经完成的Lab3控制器跟随，并提供安装、修复和记录材料的工具。当前交付的是Lab4增量补丁与文档，不包含完整模拟器、最终报告或实测通关成绩。

## 当前状态

| **项目** | **真实情况** |
| --- | --- |
| 本地目录 | GitHub归档：[hbyhby123/vnav-personal 的 lab4目录](https://github.com/hbyhby123/vnav-personal/tree/master/lab4)；本地目录未初始化.git |
| Lab3 | 用户反馈已完成稳定悬停和圆轨迹，参数为2/3/3/1 |
| Lab4实现 | 两个C++和三个launch补丁已存在 |
| 最近构建 | 用户已反馈All 20 packages succeeded；3个包有警告、无失败；尚需确认四个Part补丁已安装并进行飞行测试 |
| 运行结果 | —；尚无完整通关视频、bag或可复核成绩 |

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS / 节点 / 话题 | ROS让程序互相传消息；节点是程序，话题是传某类消息的通道 |
| catkin / rosdep | catkin负责编译ROS工程；rosdep根据清单安装系统依赖 |
| 补丁 / 依赖 | 补丁只替换部分文件；依赖是程序所需的其他库和工具 |
| launch / 增益 | launch配置启动哪些节点；增益是反馈修正误差的强度 |
| 位姿 / 航点 / yaw | 位姿是位置和朝向；航点是经过的目标位置；yaw是水平朝向角 |
| snap / QP | snap是位置四阶导数，用于衡量剧烈变化；QP是带约束的二次代价最小化问题 |
| bag / YAML / CSV | bag记录ROS消息；YAML保存参数；CSV保存表格数据 |
| TF / RViz | TF描述坐标系关系；RViz是查看机器人状态和坐标的窗口 |
| Unity / Xorg / FFmpeg | Unity是本实验场景运行器；Xorg是支持本录屏方式的桌面会话；FFmpeg是视频记录工具 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 个人题1：单段轨迹，20分 | 不同多项式次数和端点约束下怎样最省速度代价 | QP建模、求解和约束代回 | 推导PDF；本目录尚未提供答案 |
| 个人题2：多段轨迹，15分 | 需要多少参数和连接条件 | 最小snap约束计数并推广到r阶 | 推导PDF；本目录尚未提供答案 |
| Part0首门悬停 | 先验证目标和控制器接通 | 首门固定目标、零速度与零加速度 | 首门附近稳定，待实测 |
| Part1.1状态读取 | 不能从错误位置规划 | 读取当前位置与朝向，等待有效状态 | 有效轨迹起点 |
| Part1.2轨迹生成 | 依次连接赛门且避免朝向跳变 | 位置与yaw分开优化、共用时间分配 | 连续参考轨迹 |
| Part1.3轨迹跟随 | 控制器需要每个时刻的目标 | 按经过时间取目标，每秒50次发布 | 完整通关，待实测 |
| 团队采集与提交，65分含上述代码 | 让运行结果可复核 | 同轮视频、bag、参数与代码快照 | 最快完整轮次及公开链接；尚待采集 |
| 可选提速 | 完成后缩短有效通关时间 | 调整time_scale并比较完整轮次 | 真实对比记录；不预设成绩 |

## 交付文件清单

| **文件 / 目录** | **作用** | **说明** |
| --- | --- | --- |
| [README.md](README.md) | 整个项目入口 | 总览、任务、交付、环境和原理 |
| [LAB4_操作与交付清单.md](LAB4_操作与交付清单.md) | 从Lab3接着做Lab4的完整指南 | 终端顺序、截图名称、修复与演示 |
| [全部README完整内容.md](全部README完整内容.md) | 本次全部README的完整正文汇编 | 逐文件保留完整Markdown，方便复制检查 |
| [整理自检与变更清单.md](整理自检与变更清单.md) | 本次新增和修改文件清单 | 包含逐项自检、真实状态与验证边界 |
| [lab4_quickstart.zip](lab4_quickstart.zip) | 传到Ubuntu的快速操作包 | 含程序补丁、脚本、逐层README和操作指南 |
| [lab4_整理后仓库.zip](lab4_整理后仓库.zip) | 本地整理结果完整快照 | 含根文档、逐层文档和快速操作包；不含自身 |
| [lab4_quickstart/README.md](lab4_quickstart/README.md) | 快速包导航 | 说明适用前提和脚本入口 |
| [lab4_quickstart/LAB4_操作与交付清单.md](lab4_quickstart/LAB4_操作与交付清单.md) | 操作指南的随包副本 | 与根目录同名文件同步 |
| [lab4_quickstart/scripts/README.md](lab4_quickstart/scripts/README.md) | 脚本模块说明 | 安装、修复、生成、定位和记录 |
| [lab4_quickstart/scripts/install_lab4.sh](lab4_quickstart/scripts/install_lab4.sh) | 安装Lab4并构建 | 保留Lab3；新增README不复制进ROS源码目录 |
| [lab4_quickstart/scripts/repair_nlopt.sh](lab4_quickstart/scripts/repair_nlopt.sh) | 修复NLopt下载失败 | 验证压缩包后使用本地缓存，保留其他编译成果 |
| [lab4_quickstart/scripts/repair_dependencies.sh](lab4_quickstart/scripts/repair_dependencies.sh) | 修复实际出现的构建问题 | 缺gflags_catkin、catkin_simple旧缓存 |
| [lab4_quickstart/scripts/find_simulator.py](lab4_quickstart/scripts/find_simulator.py) | 定位模拟器与赛门表 | 生成~/lab4_evidence/sim.env |
| [lab4_quickstart/scripts/record_race.sh](lab4_quickstart/scripts/record_race.sh) | 同轮录像和录消息 | 保存mp4、bag、参数、源码快照和日志 |
| [lab4_quickstart/scripts/build_patch.py](lab4_quickstart/scripts/build_patch.py) | 从官方模板生成补丁 | 供维护追溯，运行会覆盖五个程序补丁 |
| [lab4_quickstart/patches/README.md](lab4_quickstart/patches/README.md) | 补丁范围与接口导航 | 不是完整ROS工作空间 |
| [lab4_quickstart/patches/planner_pkg/README.md](lab4_quickstart/patches/planner_pkg/README.md) | 首门与赛门模块说明 | 任务、接口和运行方法 |
| [lab4_quickstart/patches/planner_pkg/src/README.md](lab4_quickstart/patches/planner_pkg/src/README.md) | 首门源码说明 | 解释trajCB与main |
| [lab4_quickstart/patches/planner_pkg/src/simple_traj_planner.cpp](lab4_quickstart/patches/planner_pkg/src/simple_traj_planner.cpp) | Part0首门目标发布 | 同时发布目标坐标关系 |
| [lab4_quickstart/patches/planner_pkg/launch/README.md](lab4_quickstart/patches/planner_pkg/launch/README.md) | 首门与航点启动说明 | 明确两者启动范围与先后顺序 |
| [lab4_quickstart/patches/planner_pkg/launch/static_point_test.launch](lab4_quickstart/patches/planner_pkg/launch/static_point_test.launch) | 首门悬停启动配置 | 启动控制器、航点和首门目标节点 |
| [lab4_quickstart/patches/planner_pkg/launch/traj_gen.launch](lab4_quickstart/patches/planner_pkg/launch/traj_gen.launch) | 赛门发布启动配置 | 完整竞速时最后启动，用于触发规划 |
| [lab4_quickstart/patches/trajectory_generation_pkg/README.md](lab4_quickstart/patches/trajectory_generation_pkg/README.md) | 轨迹模块说明 | 实际ROS包名为trajectory_generation |
| [lab4_quickstart/patches/trajectory_generation_pkg/src/README.md](lab4_quickstart/patches/trajectory_generation_pkg/src/README.md) | 轨迹源码说明 | 解释三个Part、时间和边界 |
| [lab4_quickstart/patches/trajectory_generation_pkg/src/trajectory_generation_node.cpp](lab4_quickstart/patches/trajectory_generation_pkg/src/trajectory_generation_node.cpp) | Part1.1～1.3实现 | 当前位置、平滑优化、按时间发送目标 |
| [lab4_quickstart/patches/trajectory_generation_pkg/launch/README.md](lab4_quickstart/patches/trajectory_generation_pkg/launch/README.md) | 跟随器启动说明 | 控制增益和时间倍率 |
| [lab4_quickstart/patches/trajectory_generation_pkg/launch/traj_following.launch](lab4_quickstart/patches/trajectory_generation_pkg/launch/traj_following.launch) | 竞速跟随启动配置 | 启动轨迹节点和Lab3控制器 |

### 实验结束后另需提交的材料

| **文件 / 材料** | **作用** | **当前状态** |
| --- | --- | --- |
| 理论解答PDF / 综合报告PDF | 完成个人理论与实验结果说明 | —；未生成 |
| 完整controller_pkg、planner_pkg、trajectory_generation_pkg | 实际运行版本的完整源码 | —；本目录只有Lab4增量补丁，不含完整三个包 |
| 完整通关视频与最快完整一轮bag | 证明依次通过全部门并保留状态 | —；未收到 |
| rviz_drone_race.txt | 保存视频和bag的公开链接 | —；没有真实链接，因此未伪造文件 |
| 截图、参数与运行表 | 支撑报告的可复核证据 | 指南已规定文件名，实际材料尚待回传 |

## 环境与快速开始

| **步骤** | **命令 / 操作** | **说明** |
| --- | --- | --- |
| 适用环境 | Ubuntu20.04.6、ROS Noetic、Python3；已完成Lab3 | 程序命令在Ubuntu执行，不在Windows PowerShell执行 |
| 现有前提 | 保留~/vnav_ws/src/controller_pkg和已可用的bridge | 不要用官方空白Lab3覆盖已调好的控制器 |
| 首次系统工具 | sudo apt-get install -y git wget unzip python3-catkin-tools python3-rosdep autoconf automake libtool patch pkg-config libgflags-dev ffmpeg x11-utils | 需要sudo权限；完整流程见操作指南 |
| 传输快速包 | 将lab4_quickstart.zip传到Ubuntu，再unzip -n ~/Downloads/lab4_quickstart.zip -d ~/ | 路径按实际下载位置替换；旧版本先改名备份 |
| 历史NLopt下载故障 | bash ~/lab4_quickstart/scripts/repair_nlopt.sh | 当前已编译成功，无需重跑；仅同类下载错误时使用 |
| 早期依赖与缓存故障 | bash ~/lab4_quickstart/scripts/repair_dependencies.sh | 先补gflags_catkin并重建旧缓存，再继续；首次完整配置需按指南 |
| 安装程序补丁 | bash ~/lab4_quickstart/scripts/install_lab4.sh | 先备份，覆盖五个Lab4程序文件；会重新编译 |
| 场景准备 | 下载官方Lab4 Linux模拟器并解压到~/vnav-builds | 源码包不含Unity场景；链接见完整指南A4 |
| 定位场景 | python3 ~/lab4_quickstart/scripts/find_simulator.py | 生成~/lab4_evidence/sim.env |
| 每个ROS终端 | source /opt/ros/noetic/setup.bash；source ~/vnav_ws/devel/setup.bash | 分成两条命令执行 |
| 模拟器 | source ~/lab4_evidence/sim.env；cd "$(dirname "$SIM_EXEC")"；"$SIM_EXEC" | 分成三条命令执行，在独立终端保持运行 |
| 桥接 | roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch | 独立终端运行，连接Unity和ROS |
| 先测悬停 | source ~/lab4_evidence/sim.env；roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" | 两条命令；通过后Ctrl+C停止悬停测试 |
| 竞速跟随 | roslaunch trajectory_generation traj_following.launch time_scale:=2.0 | 独立终端；先使用默认2/3/3/1增益，实际仍需验证 |
| 开始记录 | bash ~/lab4_quickstart/scripts/record_race.sh | 新终端运行，等待Video and bag recording提示 |
| 最后发布赛门 | source ~/lab4_evidence/sim.env；roslaunch planner_pkg traj_gen.launch simulator_data_directory:="$SIM_DATA" | 两条命令；触发飞行，随后切回Unity |
| 正常保存 | 通过最后一门后等3秒，回录制终端按Enter | 检查视频完整、bag含两个状态话题，再判定有效轮次 |
| 再跑一轮 | 停止航点与跟随节点→Unity按R→跟随→记录→航点 | 旧轨迹不会只因按R自动重算 |

不能直接在本目录运行catkin build：这里没有完整ROS包清单和依赖。逐终端的可复制命令、截图编号和故障处理见[完整操作指南](LAB4_操作与交付清单.md)。

## 目录结构

```text
机器人集成小组项目1/
├── README.md
├── LAB4_操作与交付清单.md
├── 全部README完整内容.md
├── 整理自检与变更清单.md
├── lab4_quickstart.zip
├── lab4_整理后仓库.zip
└── lab4_quickstart/
    ├── README.md
    ├── LAB4_操作与交付清单.md
    ├── scripts/
    │   ├── README.md
    │   ├── install_lab4.sh
    │   ├── repair_dependencies.sh
    │   ├── repair_nlopt.sh
    │   ├── find_simulator.py
    │   ├── record_race.sh
    │   └── build_patch.py
    └── patches/
        ├── README.md
        ├── planner_pkg/
        │   ├── README.md
        │   ├── src/
        │   │   ├── README.md
        │   │   └── simple_traj_planner.cpp
        │   └── launch/
        │       ├── README.md
        │       ├── static_point_test.launch
        │       └── traj_gen.launch
        └── trajectory_generation_pkg/
            ├── README.md
            ├── src/
            │   ├── README.md
            │   └── trajectory_generation_node.cpp
            └── launch/
                ├── README.md
                └── traj_following.launch
```

| **目录** | **一句话说明** |
| --- | --- |
| 根目录 | 提供总览、完整操作指南、全部README正文和整理结果 |
| lab4_quickstart/ | 可传到Ubuntu使用的操作包主体 |
| scripts/ | 准备工程、修复故障、定位场景并记录实验材料 |
| patches/ | 仅包含要替换的Lab4程序文件 |
| patches/planner_pkg/ | 处理第一门目标和赛门发布配置 |
| patches/planner_pkg/src/ | 保存Part0首门悬停实现 |
| patches/planner_pkg/launch/ | 保存首门测试及赛门发布配置 |
| patches/trajectory_generation_pkg/ | 保存轨迹规划与跟随补丁 |
| patches/trajectory_generation_pkg/src/ | 保存三个Part的轨迹节点实现 |
| patches/trajectory_generation_pkg/launch/ | 保存竞速节点与控制器的联合启动配置 |

## 核心原理通俗讲解

无人机需要同时知道“飞哪里”和“怎么飞”。Lab4从赛门表取得目标位置，画出一条随时间变化的平滑路线；Lab3控制器比较目标和实际状态，再决定旋翼怎么转。桥接程序把Unity场景和ROS消息接起来。

| **阶段** | **做什么** | **为什么需要** |
| --- | --- | --- |
| 赛门输入 | 原工程读取CSV并转换到ROS坐标，发出一组位姿 | Unity与ROS对坐标的表示不同，不能直接混用 |
| 起点确认 | 读取当前位置和朝向；未收到有效状态就等 | 避免从未初始化或错误起点生成路线 |
| 位置与朝向 | 分别优化位置和yaw，并展开±π交界的角度 | 减少不必要的大幅转向 |
| 平滑优化 | 最小化snap，给每段分配时间并设置端点边界 | 使目标变化平滑；不自动保证避障、速度硬约束或完整穿门 |
| 按时间取点 | 每秒50次取当前位置、速度、加速度和朝向目标 | 让控制器持续获得下一时刻应追的状态 |
| 真实验证 | 完整视频加同轮bag、参数和源码 | 区分程序已写好与实验已完成 |

### 参数速查

| **参数** | **当前值** | **通俗解释** |
| --- | --- | --- |
| kx / kv / kr / komega | 2 / 3 / 3 / 1 | Lab3已反馈可用的四个反馈强度，Lab4仍要实测 |
| time_scale | 默认2.0 | 估计段时间乘2；大倍率分配更多时间，不代表一定通关 |
| v_max / a_max | 8.0 / 4.0 | 用于估计段时间，不是实际飞行硬上限 |
| D / N | 3 / 10 | 三维位置；每段10个系数，最高九次 |
| 发布频率 | 50Hz，即每秒50次 | 本补丁设置，区别于原框架5Hz |

## 复习与检查入口

| **要做的事** | **直接看哪里** |
| --- | --- |
| 逐终端运行、截图和演示 | [完整操作指南](LAB4_操作与交付清单.md) |
| 快速定位函数和消息 | 进入对应src/README.md |
| 查看这次到底改了什么 | [变更与自检](整理自检与变更清单.md) |
| 复制所有README完整正文 | [全部README完整内容](全部README完整内容.md) |
| 查看官方任务与基线 | [MIT Lab4要求](https://vnav.mit.edu/labs_2023/lab4/exercises.html)；[VNAV2021](https://github.com/MIT-SPARK/VNAV-labs/tree/VNAV2021/lab4) |
