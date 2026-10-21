# 实测轨迹与误差分析

## 文件用途

| 文件 | 用来做什么 |
|---|---|
| [metrics.json](metrics.json) | 完整指标与时间对齐口径 |
| [aligned_trajectory.csv](aligned_trajectory.csv) | 每个样本的目标、实际位置、位置误差与yaw误差 |
| [trajectory.png](trajectory.png) | 水平圆轨迹和三轴位置对比 |
| [tracking_errors.png](tracking_errors.png) | 三轴误差、误差范数和偏航误差 |
| [rotor_commands.png](rotor_commands.png) | 4个旋翼的转速命令 |
| [analyze_rosbag.py](analyze_rosbag.py) | 用原始bag重新计算指标 |
| [equations](equations/) | 报告的公式及题面示意图资源，不是飞行数据 |

## 怎么算的

| 项目 | 口径 |
|---|---|
| 原始数据 | [circle_tracking_20261021_081755.bag](../evidence/circle_20261021_081755/circle_tracking_20261021_081755.bag) |
| 时间对齐 | 按实际状态header时间戳排序去重；将期望状态按bag中的ROS时间线性插值到状态时刻 |
| 样本范围 | 共同时间范围全部2233个位置样本；没有按误差大小筛点 |
| 时间跨度 | 44.64秒ROS时间，约3.55圈 |
| 位置RMSE | 0.1052139米；最大0.1165955米 |
| 平均高度 / 半径 | 1.9445718米 / 5.0465593米 |
| yaw RMSE | 9.5242447度，角度差折回[-π,π] |
| 局限 | 未覆盖所有启动瞬态；消息时间关系会影响短时误差，不当作无误差标定 |

## 复算

| 步骤 | 命令 |
|---|---|
| 安装分析依赖 | `python -m pip install rosbags numpy scipy` |
| 从仓库lab3目录运行 | `python analysis/analyze_rosbag.py evidence/circle_20261021_081755/circle_tracking_20261021_081755.bag --output recomputed` |
| 查看结果 | 打开recomputed/metrics.json；该脚本不自动重画PNG |
| 返回 | [Lab3首页](../README.md) |
