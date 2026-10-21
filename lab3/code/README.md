# 最终代码与原始快照

## 运行和提交用哪个

| 位置 | 内容 | 怎么用 |
|---|---|---|
| **[controller_pkg](controller_pkg/)** | 最终完整ROS包，默认参数2、3、3、1，圆轨迹模式 | 运行和交团队源码只用这份 |
| [用户上传原始快照](original/用户上传控制器原始快照.tar.gz) | 当时上传的6个代码与配置文件，原默认值6、4、30、10 | 仅作原始记录；实际飞行当时通过命令覆盖为2、3、3、1 |
| [MIT待补全模板](original/controller_node_VNAV2021_待补全.cpp) | VNAV2021原始控制器模板 | 看11处空白原来是什么，不用于直接飞行 |
| 原课程源码 | [MIT-SPARK VNAV2021](https://github.com/MIT-SPARK/VNAV-labs/releases/tag/VNAV2021) | 查完整课程基线 |

## 三个文件分别做什么

| 文件 | 通俗作用 | Ubuntu路径 |
|---|---|---|
| [controller_node.cpp](controller_pkg/src/controller_node.cpp) | 管怎么飞：读状态、算误差、算力和力矩、发4个转速 | `~/vnav_ws/src/controller_pkg/src/controller_node.cpp` |
| [traj_publisher.cpp](controller_pkg/src/traj_publisher.cpp) | 管飞到哪：1为悬停，0为圆轨迹 | 同包src目录 |
| [traj_tracking.launch](controller_pkg/launch/traj_tracking.launch) | 管怎么启动：启动节点并设置增益 | 同包launch目录 |
| [CMakeLists.txt](controller_pkg/CMakeLists.txt) / [package.xml](controller_pkg/package.xml) | 构建与依赖信息 | 提交时保留 |
| [lab3.rviz](controller_pkg/rviz/lab3.rviz) | 保存RViz显示配置 | 提交时保留 |

## 代码边界

| 项目 | 说明 |
|---|---|
| 完整性 | 保留整个controller_pkg；不是只交一个cpp |
| 坐标约定 | ROS的z向上；按课程约定把世界系角速度转为机体系 |
| 旋翼命令 | rad/s，仿真器支持有符号转速；不直接用于真实无人机 |
| 简化 | 省略期望角速度和角加速度前馈；没有加入理论题中的阻力补偿 |
| 修改生效 | 改C++后catkin build并重启；只改launch增益则重启即可 |
| 复现步骤 | [操作与演示](../review/操作与演示.md) |
| 返回 | [Lab3首页](../README.md) |
