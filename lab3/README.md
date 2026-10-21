# Lab3 只保留这四类材料

| 入口 | 里面有什么 | 什么时候看 |
|---|---|---|
| **[交付材料 deliverables](deliverables/README.md)** | 实验报告、可编辑原稿、D1答案、D2推导PDF | 交作业、看正式结果 |
| **[复习与演示 review](review/README.md)** | 一份完整操作手册、一份速记、安装与录制脚本 | 检查前复习、现场启动 |
| **[原始数据与分析 data](data/README.md)** | 原始视频、bag、参数、截图，以及指标和曲线 | 查证据、复算误差 |
| **[代码 code](code/README.md)** | 最终完整controller_pkg、原始代码快照 | 运行实验、对照修改 |

## 任务与交付状态

| 任务 | 要做什么 | 文件 | 状态 |
|---|---|---|---|
| D1 个人10分 | 四元数转换等5问 | [deliverable_1.txt](deliverables/deliverable_1.txt) | 已准备 |
| D2 个人20分 | 旋翼分配矩阵秩、阻力补偿推导 | [deliverable_2.pdf](deliverables/deliverable_2.pdf) | 已准备 |
| D3 团队50分 | 几何控制器与稳定圆轨迹 | [controller_pkg](code/controller_pkg/) | 已实现并实际运行 |
| 飞行视频 | RViz连续绕圆至少一圈 | [40秒视频](data/raw/circle_20261021_081755/V01_RViz_circle_20261021_081755.mp4) | 已保存 |
| 综合报告 | 原理、过程、调参、实测分析 | [10页PDF](deliverables/Lab3_实验报告_黄博宇.pdf) | 已完成 |
| 官方链接文件 | Drive/Dropbox公开链接写入rviz_drone_flight.txt | 尚待真实链接 | 待补 |
| 正式提交 | 按老师要求放到指定个人与团队仓库 | 当前是个人归档 | 回执未确认 |

## 复习只记这些

| 项目 | 内容 |
|---|---|
| 核心主线 | 目标和实际做比较 → 算力与力矩 → 分配4个旋翼转速 |
| 环境 | Ubuntu20.04.6、ROS Noetic、TESSE、RViz |
| 最终参数 | kx=2、kv=3、kr=3、komega=1 |
| 圆轨迹 | 半径5米、高度2米、周期约12.57秒 |
| 实测数据 | 44.64秒ROS时间、2233个对齐位置样本、约3.55圈 |
| 位置RMSE | 0.1052米，约10.52厘米 |
| yaw RMSE | 9.524度，仍有偏航滞后 |
| 学生 | 黄博宇，24020036026，中外计科一班，第8组 |
| 本次整理 | 2026年10月22日；原始记录未改变，重复ZIP与旧版说明移出当前目录，旧版本可查Git历史 |
| 返回 | [仓库首页](../README.md) |
