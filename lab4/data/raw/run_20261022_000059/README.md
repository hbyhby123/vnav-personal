# 一次完整赛道运行

[返回上一级](../README.md)

将同轮视频、消息、参数和源码放在一起。

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 保持运行材料对应 | 将同轮视频、消息、参数和源码放在一起。 | 原bag、压缩预览与原视频分片 | 可回放和复算 |

## 交付文件

| **文件 / 目录** | **作用** |
| --- | --- |
| [original_video](original_video) | 进入下层README查看任务与逐文件清单 |
| [bag_info.txt](bag_info.txt) | 原始rosbag info输出 |
| [desired_state_publishers.txt](desired_state_publishers.txt) | 当时目标话题的发布者与订阅者 |
| [ffmpeg.log](ffmpeg.log) | 原始录像日志 |
| [parameters.yaml](parameters.yaml) | 录制时的真实ROS参数 |
| [race.bag](race.bag) | 未修改的ROS1原始消息记录 |
| [race_preview.mp4](race_preview.mp4) | 1600像素宽的连续压缩预览；不裁剪、不加速 |
| [record_start.txt](record_start.txt) | 原机器录制时间字符串，时区原样保留 |
| [rosbag.log](rosbag.log) | 原始录包日志 |
| [simple_traj_planner.cpp](simple_traj_planner.cpp) | Part0首门悬停与目标TF |
| [traj_following.launch](traj_following.launch) | 启动竞速轨迹节点与控制器，增益2/3/3/1 |
| [trajectory_generation_node.cpp](trajectory_generation_node.cpp) | Part1.1～1.3轨迹规划与采样发布 |
| [video_metadata.json](video_metadata.json) | 原/预览视频的时长、帧数、分辨率与转换命令 |
| [README.md](README.md) | 本层任务、文件、函数、输入输出、参数和通俗说明 |

## 核心代码 / 函数

| **函数名 / 文件入口** | **作用** | **通俗说明** |
| --- | --- | --- |
| race.bag | 保存5个话题 | 其中两个状态话题是必需项 |
| race_preview.mp4 | 便于网页播放 | 连续重编码，不改变速度或顺序 |
| original_video/reassemble_video.py | 恢复原视频 | 校验所有分片和最终指纹 |

## 输入 / 输出

| **方向** | **内容** | **格式 / 示例** |
| --- | --- | --- |
| 输入 | 20Hz桌面录像、ROS话题 | 同一轮run编号 |
| 输出 | 可还原原视频与消息记录 | 原bag10.7MB，原视频149508837字节 |

## 参数说明

| **参数** | **含义** | **默认值 / 实际值** |
| --- | --- | --- |
| kx/kv/kr/komega | 本轮参数 | 2/3/3/1 |
| time_scale | 本轮参数 | 2.0 |
| use_sim_time | 使用仿真时钟 | true |

## 原理通俗讲解

原视频160.75秒，bag167.28秒，二者起止记录方式不同。time_from_start给出的134.17秒是参考轨迹执行时长，不是完整录像长度，更不是独立裁判成绩。

## 验证与边界

| **项目** | **说明** |
| --- | --- |
| 实际运行 | 用户已提供20包编译成功、首门悬停与一次完整通关材料 |
| 分析 | 执行段3D RMSE约5.64cm；只有一轮，不申报最快比较 |
| 正式链接 | 视频和bag直接上传作业平台，无需外部链接 |
