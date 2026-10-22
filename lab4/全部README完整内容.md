# Lab4 全部README完整内容

## lab4_quickstart/patches/planner_pkg/launch/README.md

````markdown
# 首门与航点启动配置

[返回上一级](../README.md)

两个launch分别用于首门验证和完整竞速前的赛门发布。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| 航点 | 希望依次经过的目标位置 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 静态测试 | 同时接好目标、控制器和赛门 | static_point_test.launch | 启动首门悬停链路 |
| 发布整组赛门 | 给竞速节点提供路线输入 | traj_gen.launch | 触发轨迹生成 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 启动顺序和参数 |
| [static_point_test.launch](static_point_test.launch) | 启动controller_node、traj_vertices_publisher、simple_traj_planner |
| [traj_gen.launch](traj_gen.launch) | 只启动traj_vertices_publisher |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| static_point_test.launch | 启动悬停相关节点 | 用于Part0，竞速前先停止 |
| traj_gen.launch | 启动赛门发布节点 | 必须等跟随器与记录器准备好再启动 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | simulator_data_directory | 场景_Data目录，里面有StreamingAssets/赛门CSV |
| 输入 | 控制器增益 | 仅static_point_test.launch设置 |
| 输出 | 运行节点和/desired_traj_vertices消息 | 航点由官方节点读取和发布 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| simulator_data_directory | 实际场景路径；两文件共有 | $(env HOME)/vnav-builds/vnav-2021-lab4/vnav-2021-lab4_Data |
| kx / kv | 位置和速度误差的反馈强度 | 2 / 3 |
| kr / komega | 朝向和转动速度的反馈强度 | 3 / 1 |

## 原理通俗讲解

launch像开机清单：告诉ROS开哪些程序、把哪些参数交给它们。赛门数据路径应来自路径识别脚本，不能照抄错误的解压目录。static_point_test会启动控制器，因此它与竞速跟随启动文件不能同时运行。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 悬停 | roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" |
| 竞速触发 | roslaunch planner_pkg traj_gen.launch simulator_data_directory:="$SIM_DATA" |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/patches/planner_pkg/README.md

````markdown
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
````

## lab4_quickstart/patches/planner_pkg/src/README.md

````markdown
# 首门目标源码

[返回上一级](../README.md)

simple_traj_planner.cpp补齐Part0，读取第一门并发布固定目标。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| catkin | ROS工程使用的编译工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 回调 | 收到消息后自动执行的函数 |
| PoseArray | 一组位置和朝向 |
| MultiDOFJointTrajectoryPoint | 一个时刻的期望位置、朝向、速度和加速度消息 |
| TF | 描述两个坐标系相对位置和朝向的消息 |
| bag | 记录ROS消息的原始数据文件 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 读取首门 | 从赛门列表找初始测试目标 | 检查空列表后取front() | 有有效目标 |
| 发布悬停状态 | 控制器需要完整目标消息 | 位置、朝向、零速度和零加速度 | 控制器能接收目标 |
| 广播目标坐标 | 便于RViz定位目标 | 发布world到desired_pose的TF | 可以查看目标位置 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 源码解释 |
| [simple_traj_planner.cpp](simple_traj_planner.cpp) | Part0实现与ROS入口 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| trajCB(const geometry_msgs::PoseArray&) | 收到赛门就处理 | 只取第一个Pose，填充并发布目标与TF |
| main(int, char**) | 启动simple_traj_planner | 订阅赛门并等待回调；回调是收到消息后自动执行的函数 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | desired_traj_vertices | PoseArray；根命名空间下即/desired_traj_vertices |
| 输出 | desired_state | MultiDOFJointTrajectoryPoint |
| 输出 | world → desired_pose | 目标TF，使用当前ROS时间 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 目标下标 | 选哪一道赛门 | 0，即第一门 |
| time_from_start | 固定目标的相对时间 | 0秒 |
| 期望速度与加速度 | 到目标后保持 | 全为0 |
| 订阅/发布队列 | 最多缓存的消息数 | 10 / 1 |

## 原理通俗讲解

它相当于给控制器一个固定目的地。程序不会自己算旋翼转速，也不负责判断是否穿过所有门；实际飞行由已有控制器完成。空列表时直接返回，避免访问不存在的第一门。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 构建 | 安装后在~/vnav_ws运行catkin build |
| 运行 | 通过../launch/static_point_test.launch启动 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/patches/README.md

````markdown
# Lab4 程序补丁总览

[返回上一级](../README.md)

这里只保存要替换的程序文件；其余源码和依赖由安装脚本从官方工程补齐。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 补丁 | 替换原工程中一部分文件的修改 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| 位姿 | 位置加朝向 |
| 航点 | 希望依次经过的目标位置 |
| PoseArray | 一组位置和朝向 |
| Odometry | 包含实际位置、朝向和速度的状态消息 |
| MultiDOFJointTrajectoryPoint | 一个时刻的期望位置、朝向、速度和加速度消息 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |
| time_scale | 把估计飞行时间乘一个倍率；数值大时分配的时间更长 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 首门验证 | 先检查目标与控制器是否接通 | planner_pkg静态目标 | 第一门附近稳定悬停，待实测 |
| 轨迹跟随 | 让无人机依次经过赛门 | trajectory_generation_pkg轨迹节点 | 完整通关，待实测 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 补丁范围和接口说明 |
| [planner_pkg/](planner_pkg/) | 首门目标源码及两份启动文件 |
| [trajectory_generation_pkg/](trajectory_generation_pkg/) | 轨迹源码及一份启动文件 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| trajCB() | 生成首门悬停目标 | 只取第一道门 |
| WaypointFollower | 轨迹生成和目标发布类 | 读取赛门并持续发送目标 |
| launch文件 | 一次启动关联节点 | launch就是节点与参数的启动配置 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 官方工程、已有controller_pkg、桥接器和场景CSV | 本目录不含package.xml和CMakeLists.txt |
| 消息输入 | /desired_traj_vertices、/current_state | PoseArray、Odometry |
| 消息输出 | /desired_state | MultiDOFJointTrajectoryPoint |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 位置维度 | 每个点含x、y、z | 3 |
| 控制增益 | 两类启动文件沿用Lab3参数 | 2/3/3/1 |
| time_scale | 竞速段时间倍率 | 2.0 |

## 原理通俗讲解

补丁是只替换工程的一部分。航点是必须经过的目标位置；优化器把这些点连成平滑的时间曲线；控制器再追这条曲线。PoseArray是一组位姿，Odometry包含实际位置、朝向和速度，MultiDOFJointTrajectoryPoint包含某一时刻的期望状态。这里没有完整ROS包定义，必须安装到官方工作空间后编译。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 安装 | 使用../scripts/install_lab4.sh，不在patches目录直接编译 |
| 复习 | 先看planner_pkg，再看trajectory_generation_pkg |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/patches/trajectory_generation_pkg/launch/README.md

````markdown
# 竞速跟随启动配置

[返回上一级](../README.md)

启动轨迹节点和已有控制器，并传入增益及时间倍率。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 节点 | 一个正在工作的ROS程序 |
| 航点 | 希望依次经过的目标位置 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |
| time_scale | 把估计飞行时间乘一个倍率；数值大时分配的时间更长 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 启动跟随 | 把规划与控制接起来 | 启动两个节点 | 等待赛门消息 |
| 设置速度节奏 | 第一次先以较慢时间分配运行 | time_scale倍率 | 先验证完整通关 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 启动和参数说明 |
| [traj_following.launch](traj_following.launch) | 两个节点和可覆盖参数 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| trajectory_generation_node | 生成与发布期望状态 | 接收赛门和实际状态 |
| controller_node | 沿用Lab3控制器 | 读取目标后算旋翼命令 |
| time_scale参数 | 传给轨迹节点的私有参数 | 私有参数是只供这个节点使用的设置 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | kx、kv、kr、komega、time_scale | roslaunch参数 |
| 输出 | 两个运行节点及/desired_state | 还需要bridge与航点发布器 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| kx / kv | 位置与速度反馈增益 | 2.0 / 3.0 |
| kr / komega | 姿态与角速度反馈增益 | 3.0 / 1.0 |
| time_scale | 估计段时间倍率 | 2.0；需根据实际飞行调整 |

## 原理通俗讲解

这个文件只负责把程序启动并把设置传进去，不直接计算轨迹。启动后先等记录器准备好，再发布赛门。它已经启动controller_node，不能再同时启动Lab3的traj_tracking.launch或首门测试，以免多个程序抢着发目标或旋翼命令。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 启动 | roslaunch trajectory_generation traj_following.launch kx:=2 kv:=3 kr:=3 komega:=1 time_scale:=2.0 |
| 之后 | 先运行record_race.sh，看到记录就绪后发布赛门 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/patches/trajectory_generation_pkg/README.md

````markdown
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
````

## lab4_quickstart/patches/trajectory_generation_pkg/src/README.md

````markdown
# 轨迹节点源码

[返回上一级](../README.md)

WaypointFollower把当前位置、赛门和时间连起来，持续产生期望状态。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 节点 | 一个正在工作的ROS程序 |
| 定时器 | 按固定间隔执行函数的工具 |
| 航点 | 希望依次经过的目标位置 |
| PoseArray | 一组位置和朝向 |
| Odometry | 包含实际位置、朝向和速度的状态消息 |
| yaw | 从上往下看时无人机面向的角度 |
| snap | 位置的四阶导数；最小化它用于抑制猛烈的轨迹变化 |
| bag | 记录ROS消息的原始数据文件 |
| time_scale | 把估计飞行时间乘一个倍率；数值大时分配的时间更长 |
| Hz | 每秒发生多少次；50Hz就是每秒50次 |
| 四元数 | 用四个数表达三维朝向的方法 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| Part1.1 | 确认无人机当前在哪儿 | 读取Odometry位置与yaw | 有效起点 |
| Part1.2 | 从起点平滑连接全部门 | 顶点约束、角度展开、最小snap | 优化轨迹 |
| Part1.3 | 按当前进度发送正确目标 | ROS经过时间采样并限制到终点 | 目标随时间推进 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 逐函数说明 |
| [trajectory_generation_node.cpp](trajectory_generation_node.cpp) | 轨迹节点全部实现 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| onCurrentState() | 更新x和current_yaw | 标记have_current，拒绝无效起点 |
| generateOptimizedTrajectory() | 建立位置与yaw顶点并求解 | 起终点设置静止边界，中间点指定位置和朝向 |
| publishDesiredState() | 求位置、速度、加速度和姿态 | 填充消息数组并发布 |
| WaypointFollower() | 注册订阅者和50Hz定时器 | 定时器是按固定间隔调用函数的工具 |
| main() | 初始化ROS并持续处理消息 | 调用ros::spin()等待消息 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | /current_state | Odometry中的位置和四元数；四元数是用四个数保存三维朝向的表示 |
| 输入 | /desired_traj_vertices | 门的PoseArray |
| 输出 | /desired_state | transforms、velocities、accelerations各含一个元素 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| D | 位置维度 | 3 |
| N | 每段系数数目 | 10，最高九次 |
| v_max / a_max | 原框架用于估计段时间的参数 | 8.0 / 4.0，非实际飞行硬限幅 |
| time_scale | 估计段时间再乘的倍率 | 2.0 |
| 采样时间 | 现在减轨迹开始时间 | 限制在0到轨迹总时长 |
| 生成条件 | 是否重算已有轨迹 | 已有轨迹时返回，需要重启节点开始新一轮 |

## 原理通俗讲解

航点像路线上的钉子，优化器用平滑曲线穿过它们。程序把位置和朝向分开算，但用相同段时间，让它们在同一时刻到同一道门。随后每秒50次从曲线上取目标。到终点后保持末端，不再向越界时间求值。最小snap是平滑目标，不等于最短时间或避障保证。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 查看Part | 源文件保留Part1.1、1.2、1.3标记 |
| 重跑 | 停跟随器、停航点、复位Unity，再按记录顺序启动 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/README.md

````markdown
# Lab4 快速操作包

[返回上一级](../README.md)

把Lab4补丁、安装修复和实验采集放在一起，方便从已经完成的Lab3继续。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| catkin | ROS工程使用的编译工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 补丁 | 替换原工程中一部分文件的修改 |
| launch | 列出要启动哪些程序及其参数的配置文件 |
| 航点 | 希望依次经过的目标位置 |
| YAML | 用键和值保存参数的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| 增益 | 把误差转换为控制修正量时的反馈强度 |
| time_scale | 把估计飞行时间乘一个倍率；数值大时分配的时间更长 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 安装与修复 | 缺依赖或缓存指向旧路径 | 脚本备份并重建 | 能够继续编译检查 |
| 飞行与采集 | 需要按赛门飞行并留证据 | 航点优化、目标发布、视频和数据记录 | 获得待核验的完整运行材料 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 快速包入口 |
| [LAB4_操作与交付清单.md](LAB4_操作与交付清单.md) | 按终端分步操作和截图清单 |
| [patches/](patches/) | 两个C++和三个launch补丁，逐层附README |
| [scripts/](scripts/) | 安装、修复、定位模拟器、录制和生成补丁脚本 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| install_lab4.sh | 安装五个程序补丁 | 保留现有Lab3控制器，备份后编译 |
| repair_dependencies.sh | 修复已出现的依赖和缓存问题 | 补gflags_catkin，再重新构建 |
| record_race.sh | 采集同轮材料 | 一起保存视频、bag和参数 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 已有Lab3工作空间、官方VNAV2021源码、Lab4模拟器 | Ubuntu20.04 / ROS Noetic |
| 输出 | ~/vnav_ws内Lab4文件；~/lab4_evidence内备份与运行材料 | 源码、日志、mp4、bag、YAML |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 工作空间 | 现有ROS源码与构建目录 | ~/vnav_ws |
| 控制器增益 | Lab3反馈可稳定运行的一组参数 | kx=2、kv=3、kr=3、komega=1 |
| time_scale | 把估计飞行时间乘一个倍率 | 2.0 |

## 原理通俗讲解

ROS是让各程序互相传消息的工具。先让原有控制器继续负责“怎么飞”，再装入Lab4负责“飞哪里”的程序，最后记录实际飞行。包内是增量补丁，不含完整依赖或模拟器，不能直接在这个目录运行catkin build。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 准备 | 先读[完整指南](LAB4_操作与交付清单.md)，确认Lab3可用 |
| 安装 | bash ~/lab4_quickstart/scripts/install_lab4.sh |
| 当前报错修复 | bash ~/lab4_quickstart/scripts/repair_dependencies.sh |
| 模拟器定位 | python3 ~/lab4_quickstart/scripts/find_simulator.py |
| 录像和数据 | bash ~/lab4_quickstart/scripts/record_race.sh |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## lab4_quickstart/scripts/README.md

````markdown
# 安装、修复与数据采集脚本

[返回上一级](../README.md)

这里负责把实验准备好、把故障日志和运行材料保存下来。

## 阅读前先懂这些词

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让不同程序互相传消息的工具 |
| catkin | ROS工程使用的编译工具 |
| rosdep | 根据包清单安装系统依赖的工具 |
| 依赖 | 程序运行或编译所需的其他库和工具 |
| 补丁 | 替换原工程中一部分文件的修改 |
| 节点 | 一个正在工作的ROS程序 |
| 航点 | 希望依次经过的目标位置 |
| CSV | 用分隔符保存表格数据的文本格式 |
| bag | 记录ROS消息的原始数据文件 |
| FFmpeg | 用于命令行录制视频的工具 |
| Xorg | 支持本项目桌面录制方式的显示会话 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 安装补丁 | Lab4代码和依赖未放好 | 保留Lab3，备份后安装并构建 | 得到可继续验证的工作空间 |
| 修复缓存 | 依赖搬动后仍指向旧目录 | 补gflags_catkin、备份build/devel后重建 | 解决已报告的路径与缺包问题 |
| 采集材料 | 视频与飞行数据容易对不上 | 同轮保存视频、bag、参数和代码 | 便于复盘和计算误差 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [README.md](README.md) | 脚本索引 |
| [install_lab4.sh](install_lab4.sh) | 首次安装Lab4补丁，需已有工具和Lab3 |
| [repair_nlopt.sh](repair_nlopt.sh) | 修复NLopt下载失败并继续编译 |
| [repair_dependencies.sh](repair_dependencies.sh) | 修复缺gflags_catkin和旧构建缓存 |
| [find_simulator.py](find_simulator.py) | 识别场景路径，生成sim.env |
| [record_race.sh](record_race.sh) | 命令行录屏与录bag |
| [build_patch.py](build_patch.py) | 从官方模板重新生成五个补丁文件，仅供维护 |

## 核心代码 / 函数

| **函数名 / 入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| install_lab4.sh：主流程 | 备份、去重、安装、构建 | 只复制指定的五个程序文件 |
| repair_dependencies.sh：主流程 | 补源码依赖并重建 | 不修改src内实验代码 |
| find_simulator.py：主流程 | 找到赛门CSV和可执行文件 | 只接受唯一有效场景 |
| record_race.sh：finish() | 结束录像和录包 | 等待写完，再输出保存位置 |
| build_patch.py：主流程 | 下载模板并填充Part | 会覆盖patches内五个程序文件，平时无需运行 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 已完成的Lab3、网络、Xorg桌面和正在运行的ROS节点 | Xorg是可供脚本录制桌面的显示会话 |
| 输出 | ~/lab4_evidence/backups与logs | 备份目录、txt日志 |
| 输出 | ~/lab4_evidence/sim.env | SIM_EXEC、SIM_DATA两项Shell变量 |
| 输出 | ~/lab4_evidence/runs/run_时间/ | race.mp4、race.bag、parameters.yaml、bag_info.txt、代码快照和日志 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 录屏帧率 | 每秒保存多少帧画面 | 20 |
| 准备时间 | 录屏启动前摆好窗口的时间 | 5秒；前面另有2秒录包存活检查 |
| 停止方式 | 飞行结束后正常保存 | 回录制终端按Enter |
| 重建并发 | 修复脚本控制编译资源 | -j2 -p1 |
| 日志 | 安装/修复的记录位置 | ~/lab4_evidence/logs |

## 原理通俗讲解

catkin是ROS的编译工具；build和devel保存编译产物，不是手写源码。搬动依赖后旧产物记住了错误路径，就先备份再重建。gflags_catkin是把参数处理库接入catkin的源码包。rosdep根据包内清单安装系统依赖。FFmpeg负责录桌面，rosbag负责记录消息，二者放进同一轮目录以免拿错。

## 操作与检查

| **步骤** | **命令 / 操作** |
| --- | --- |
| 安装 | bash ~/lab4_quickstart/scripts/install_lab4.sh |
| NLopt下载修复 | bash ~/lab4_quickstart/scripts/repair_nlopt.sh |
| 依赖与缓存修复 | bash ~/lab4_quickstart/scripts/repair_dependencies.sh |
| 定位 | python3 ~/lab4_quickstart/scripts/find_simulator.py |
| 录制 | 先启跟随器，再运行record_race.sh，最后发布航点 |

## 验证状态

| **检查** | **现状** |
| --- | --- |
| 文件与接口 | 依据当前仓库源码整理 |
| Ubuntu编译与完整通关 | 用户已反馈20个包全部编译成功；完整通关仍待实测，当前源码是否已安装四个Part补丁需检查 |
| 报告与成绩 | —；等待真实视频、bag和运行记录 |
````

## README.md

````markdown
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
````
