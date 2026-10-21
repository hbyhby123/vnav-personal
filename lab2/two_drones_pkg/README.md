# two_drones_pkg 文件说明

| 文件 | 做什么 |
|---|---|
| [src/frames_publisher_node.cpp](src/frames_publisher_node.cpp) | 发布双无人机动态坐标变换 |
| [src/plots_publisher_node.cpp](src/plots_publisher_node.cpp) | 发布无人机和轨迹可视化信息 |
| [launch/two_drones.launch](launch/two_drones.launch) | 一起启动实验节点，支持静态场景选项 |
| [config/default.rviz](config/default.rviz) | 保存RViz显示配置 |
| [mesh/quadrotor.dae](mesh/quadrotor.dae) | 无人机外观模型 |
| [CMakeLists.txt](CMakeLists.txt) | 构建配置 |
| [package.xml](package.xml) | ROS软件包信息与依赖 |
| [完整实验报告](../Lab2_实验报告.md) | 启动方法、数学推导与历史运行结果 |
