# 原始记录与计算结果

## 原始文件保持不变

| 位置 | 内容 | 用途 |
|---|---|---|
| [视频](raw/circle_20261021_081755/V01_RViz_circle_20261021_081755.mp4) | 40秒、15fps的RViz画面 | 下载后播放完整绕圆 |
| [ROSbag](raw/circle_20261021_081755/circle_tracking_20261021_081755.bag) | 目标、状态、转子命令与时钟 | 复算轨迹误差 |
| [参数](raw/circle_20261021_081755/parameters_20261021_081755.txt) | kx=2、kv=3、kr=3、komega=1 | 确认录制时用的参数 |
| [完整性清单](raw/circle_20261021_081755/manifest.json) | 3个原文件的字节数与SHA-256 | 校验原文件未改变 |
| [初次翻转故障bag](raw/hover_debug.bag) | 初始高增益造成翻转时的原始记录 | 与最终稳定圆轨迹数据分开，供复习排错 |
| [原始截图](raw/screenshots/) | 01、02、03、04、05、06、06B、07，共8张 | 环境、编译、仿真、悬停和绕圆证据 |

## 分析结果与复算

| 文件 | 说明 |
|---|---|
| [metrics.json](analysis/metrics.json) | 时间范围、样本数、RMSE与完整统计口径 |
| [aligned_trajectory.csv](analysis/aligned_trajectory.csv) | 每个样本的目标、实际位置、误差和yaw误差 |
| [trajectory.png](analysis/trajectory.png) | 期望与实际轨迹 |
| [tracking_errors.png](analysis/tracking_errors.png) | 位置与偏航误差 |
| [rotor_commands.png](analysis/rotor_commands.png) | 4个旋翼的命令变化 |
| [analyze_rosbag.py](analysis/analyze_rosbag.py) | 安装rosbags、numpy、scipy后可重新计算指标 |
| 从Lab3目录复算 | `python data/analysis/analyze_rosbag.py data/raw/circle_20261021_081755/circle_tracking_20261021_081755.bag --output recomputed` |
| 时间口径 | 实际状态header时间与期望消息ROS记录时间对齐，线性插值；共同范围全部2233点，未按误差筛点 |
| 结果 | 44.64秒，约3.55圈；位置RMSE约10.52厘米，yaw RMSE约9.52度 |
| 截图06B | 原图读数1.952798米，文件名沿用；另一次终端读数为1.957025米，单次读数不等于RMSE |
| 返回 | [Lab3首页](../README.md) |
