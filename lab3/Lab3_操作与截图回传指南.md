# Lab 3 小白操作与检查复习指南

适用：Ubuntu 20.04.6、ROS Noetic、VNAV2021源码。更新日期：2026年10月21日。

## 一、先看你现在做到哪了

| 事情 | 目前状态 |
|---|---|
| Ubuntu和ROS环境 | 已确认符合要求 |
| 下载实验代码、安装依赖 | 已完成 |
| 编译8个ROS包 | 已成功 |
| 下载TESSE仿真器lab3.zip | 正在下载，等100%并出现终端提示符 |
| 启动仿真器、桥接、RViz | 接下来做 |
| 补全控制器、悬停和绕圆 | 尚未完成 |
| 理论题、视频和最终报告 | 后续完成 |

记住：编译通过只说明程序能构建。原始controller_node.cpp里还有待填代码，不能把“编译成功”当作“无人机已完成绕圆”。

## 二、最后到底交什么

| 任务 | 通俗解释 | 交付物 |
|---|---|---|
| D1，个人10分 | 回答5道四元数转换小题 | deliverable_1.txt |
| D2，个人20分 | 解释一种旋翼配置为什么不能正常控制；说明如何补偿空气阻力 | 带数学推导的PDF |
| D3，团队50分 | 把控制器补完整，让无人机稳定绕圆 | 整个controller_pkg文件夹 |
| D3视频 | RViz中连续飞完一圈 | 视频上传Drive或Dropbox，公开链接写入rviz_drone_flight.txt |
| 本校实验报告 | 把原理、步骤、截图、结果写清楚 | 按老师要求交Word或PDF |

官方列出的三项合计80分。截图是写报告和检查时的证据，不能替代源码和视频。MIT网页中的2023年截止日期是历史信息。你准备的检查日期按当前对话为2026年10月23日，以老师通知为准。

## 三、操作前只记三条

1. 所有命令都在Ubuntu终端输入。每个代码框逐行执行，出错就停在那一行。
2. 出现by@ubuntu:...$，代表这一条命令已结束，才输入下一条。下载停在48%时继续等。
3. 报错时发“输入的命令＋完整错误”，不要反复重装全部软件。

## 四、从这里继续：下载、解压、启动仿真器

### 第1步：等下载完成

你已经执行：

```bash
cd ~/vnav-builds
wget https://vnav.mit.edu/material/lab3.zip
```

成功标志：进度100%，提示文件保存成功，重新出现终端提示符。

如果下载中断，用下面命令续传，不用重新下载：

```bash
cd ~/vnav-builds
wget -c https://vnav.mit.edu/material/lab3.zip
```

### 第2步：查看压缩包

```bash
cd ~/vnav-builds
unzip -l lab3.zip | head -25
```

这一步只查看里面的文件名。若提示unzip命令不存在，先执行：

```bash
sudo apt install unzip
```

### 第3步：解压并找启动程序

你之前的~/vnav-builds/lab3为空，可以执行：

```bash
cd ~/vnav-builds
unzip -n lab3.zip
find ~/vnav-builds -type f -name 'lab3.x86_64'
```

unzip -n表示已有同名文件时保留原文件。不要只复制.x86_64，旁边的数据文件也要保留。

成功标志：find输出程序完整路径。通常应为/home/by/vnav-builds/lab3/lab3.x86_64。

如果路径不同，把find输出发我；后面cd要进入程序实际所在目录。若没找到，不继续启动。

### 第4步：启动仿真器——终端A

确认上一步路径后，通常执行：

```bash
cd ~/vnav-builds/lab3
chmod +x lab3.x86_64
./lab3.x86_64
```

成功标志：弹出Unity窗口，看到无人机。这个终端保持打开。

截图03：TESSE仿真器初始场景。现在无人机不飞很正常，控制器还没补完。

仿真器按键：W开启旋翼，R重置无人机位置。重置前先在控制器终端按Ctrl+C停掉控制器。

## 五、把仿真器和ROS连起来

按Ctrl+Alt+T新开终端。终端A继续保持运行。

### 第5步：启动桥接——终端B

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch
```

桥接可以理解成“翻译员”：把仿真器状态送给ROS，把ROS的旋翼命令送回仿真器。终端保持打开。

### 第6步：打开观察窗口——终端C

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roscd controller_pkg
rviz -d rviz/lab3.rviz
```

成功标志：RViz中能看到坐标轴与无人机状态，world是世界坐标系，base_link_gt是无人机机身坐标系。

截图04：RViz坐标系与状态。若RViz黑屏或显示红色错误，截完整界面发我。

## 六、补全控制器：这一步不能省

原始文件是：~/vnav_ws/src/controller_pkg/src/controller_node.cpp。

代码要做的事情只有这一条主线：

期望位置和实际位置 → 算误差 → 算需要的力与力矩 → 分配给四个旋翼 → 发转速命令。

待补全的内容包括：订阅期望/当前状态，读取状态，计算位置和姿态误差，计算推力与力矩，按旋翼编号分配转速并发布。转速单位是rad/s。当前角速度要按代码要求从世界系转到机体系。仿真器允许有符号转速，应按原始代码要求处理。

我已拿到公开原始代码，不用重复上传。到这一步时，把仿真器和RViz的结果发来，我会继续给你对应版本的代码修改与替换步骤。此指南还没有包含完整控制器实现，不能跳过这一步直接认定飞行成功。

替换前先备份：

```bash
cp ~/vnav_ws/src/controller_pkg/src/controller_node.cpp ~/lab3_evidence/controller_node_original.cpp
```

每次修改C++源码后都编译：

```bash
cd ~/vnav_ws
catkin build
source ~/vnav_ws/devel/setup.bash
```

成功标志：Summary显示全部成功，Failed为None。截图05。

## 七、先定点悬停，再绕圆

### 第7步：先测试悬停

打开轨迹文件：

```bash
gedit ~/vnav_ws/src/controller_pkg/src/traj_publisher.cpp
```

把文件上方这一行：

```cpp
#define STATIC_POSE 0
```

改成：

```cpp
#define STATIC_POSE 1
```

保存，重新执行上面的编译命令。

保持终端A、B、C运行，再开终端D：

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roslaunch controller_pkg traj_tracking.launch
```

代码补全后，目标是飞到(0,0,2)米附近并保持，期望yaw为45度。观察约20—30秒，截图06。这个观察时长是建议，不是官方评分阈值。

### 第8步：切换绕圆

1. 在终端D按Ctrl+C，停止控制器和轨迹发布器。
2. 把STATIC_POSE改回0，保存并重新编译。
3. 在Unity窗口按R重置，必要时按W开启旋翼。
4. 在终端D重新执行roslaunch controller_pkg traj_tracking.launch。

原始代码给定的轨迹是：

| 参数 | 数值 |
|---|---|
| 圆心的水平位置 | x=0，y=0 |
| 半径 | 5米 |
| 高度 | 2米 |
| 一圈时间 | 约12.6秒 |
| yaw | 随时间变化 |

刚启动时有快速切入动作，重点观察之后能否连续稳定绕圆。截图07俯视效果，截图08三维效果。若没有历史轨迹曲线，先保留期望/实际位姿与视频，不要拼造轨迹图。

### 调参怎么记

参数文件：~/vnav_ws/src/controller_pkg/launch/traj_tracking.launch。

| 参数 | 通俗含义 |
|---|---|
| kx | 偏离目标位置时，拉回去的力度 |
| kv | 速度误差反馈，也帮助抑制平移振荡 |
| kr | 机身姿态偏离目标时，纠正的力度 |
| komega | 旋转速度误差反馈，也帮助抑制转动振荡 |

默认四个值都是1，不能保证已经合适。先检查公式、坐标和转子顺序，再调增益。一次只改一项，记录“旧值、新值、现象”。仅修改launch参数时，保存并重启终端D即可；修改C++后才需要重新编译。

## 八、录视频、数据，保存最终代码

### 第9步：检查三个话题——新开终端E

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
rostopic type /desired_state
rostopic type /current_state
rostopic type /rotor_speed_cmds
rostopic echo -n 1 /rotor_speed_cmds
```

依次应是trajectory_msgs/MultiDOFJointTrajectoryPoint、nav_msgs/Odometry、mav_msgs/Actuators。最后能看到4个旋翼转速，不应出现nan或inf。截图09。

### 第10步：录制完整一圈视频

在RViz中录屏，稳定后录30秒左右，覆盖至少一整圈。保存为：

V01_RViz无人机连续完成完整圆轨迹跟踪.mp4

上传Google Drive或Dropbox，设为知道链接的人可查看，用无痕浏览器测试无需登录即可观看。把真实链接写入rviz_drone_flight.txt，截图10。

### 第11步：建议同时录数据

先执行：

```bash
mkdir -p ~/lab3_evidence
```

控制器稳定绕圆时，在终端E执行：

```bash
rosbag record -O ~/lab3_evidence/circle_tracking.bag /desired_state /current_state /rotor_speed_cmds /clock
```

录约30秒后，在终端E按Ctrl+C结束。bag是实际飞行数据，我可以用它画轨迹和误差曲线。不要在控制器终端按Ctrl+C，以免停错程序。

### 第12步：打包最终代码

```bash
cd ~/vnav_ws/src
tar -czf ~/lab3_evidence/controller_pkg_final.tar.gz controller_pkg
```

## 九、截图完整命名表

01—10是建议保留的报告证据；11可选；12由我根据数据生成。官方必须交的是源码和视频等交付物，不是这12张截图。

| 编号 | 直接用这个文件名 | 画面要有什么 |
|---|---|---|
| 01 | 01_Ubuntu20.04与ROS_Noetic版本及Lab3工作空间源码目录.png | 系统版本、ROS版本、src下各目录 |
| 02 | 02_Lab3原始工程首次catkin_build编译成功摘要.png | All 8 packages succeeded、Failed None |
| 03 | 03_TESSE_Unity仿真器启动后的无人机初始场景.png | Unity窗口与无人机 |
| 04 | 04_RViz显示world与base_link_gt坐标系及无人机状态.png | 坐标轴、状态和左侧显示列表 |
| 05 | 05_补全几何控制器后整个工作空间编译成功摘要.png | 修改控制器后的成功摘要 |
| 06 | 06_STATIC_POSE定点模式下无人机期望与实际位姿对比.png | 期望点与实际无人机位姿 |
| 07 | 07_RViz俯视视角下无人机圆轨迹跟踪与期望轨迹对比.png | 俯视的期望与实际轨迹或位姿 |
| 08 | 08_RViz三维视角下无人机圆轨迹跟踪与飞行高度展示.png | 三维视角、飞行高度和坐标轴 |
| 09 | 09_期望状态当前状态转子指令话题类型及四旋翼转速输出.png | 三种消息类型和4个转子转速 |
| 10 | 10_无痕浏览器无需登录播放RViz完整绕圆视频验证.png | 实际可播放的视频页面 |
| 11 | 11_不同控制增益下圆轨迹跟踪效果及参数对比.png | 实际做过的调参前后效果和参数 |
| 12 | 12_基于实测ROSbag的XYZ位置误差及误差范数曲线.png | 后续由实际数据生成 |

补截图01可执行：

```bash
lsb_release -d
rosversion -d
ls ~/vnav_ws/src
```

截图方法：Ubuntu按Shift+PrtSc框选；笔记本可能还要加Fn。也可在Windows按Win+Shift+S截虚拟机区域并保存。

## 十、后天检查前的安排

| 时间 | 优先完成什么 | 留下的证据 |
|---|---|---|
| 今天（10月21日） | 启动仿真、桥接、RViz；推进控制器实现和悬停 | 截图03—06、可编译代码 |
| 明天（10月22日） | 圆轨迹稳定运行、调参、录完整一圈视频与数据 | 截图07—10、视频、bag、最终代码 |
| 检查前（10月23日） | 复跑启动顺序、核对理论题与交付文件、复习下面的问题 | 本地能演示、文件齐全、链接可看 |

这是推进顺序，飞行成功仍要以实际运行结果为准。若今天遇到故障，先解决它，不为凑截图跳过。

## 十一、检查时你要能讲明白的8句话

1. 实验目标：让四旋翼根据目标轨迹，自动调整四个旋翼转速，稳定跟踪圆轨迹。
2. 轨迹生成：traj_publisher已经提供期望位置、速度、加速度和朝向；我主要补全几何控制器。
3. 三个话题：desired_state给目标，current_state给实际状态，rotor_speed_cmds发转速。
4. 闭环控制：目标和实际有误差，控制器不断纠正，每个周期重新计算命令。
5. 为什么四个转速不同：转速差产生滚转、俯仰、偏航力矩；总升力决定向上的推力。
6. 为什么先悬停：先排查力方向、坐标系、旋翼顺序和姿态控制，再增加圆轨迹的难度。
7. 几何控制是什么：直接用旋转矩阵描述并控制姿态，避免依赖欧拉角表示产生的奇异问题。
8. 怎么证明完成：成功编译、真实稳定飞行、RViz完整一圈视频，加上实际数据或截图。

不要把“已编译”“已悬停”“已绕圆”混成同一件事。老师问到没做过的调参或指标，说明实际进度即可。

理论题再记两点：D2-A通过比较分配矩阵的秩判断控制通道是否独立；D2-B根据机体系速度估计阻力，再转换到控制使用的坐标系进行补偿。具体矩阵与正负号要按题目原图推导。

## 十二、常见问题，按现象处理

| 现象 | 先怎么做 |
|---|---|
| 下载仍显示百分比 | 等到100%和终端提示符，不输入后续命令 |
| chmod提示No such file | ls看目录；find寻找lab3.x86_64，先确认解压路径 |
| 找不到mav_msgs | 检查src/mav_comm是否下载；本次你已经补好 |
| catkin提示全部成功，但有CMP0048警告 | 本次不影响编译，可继续 |
| roslaunch提示找不到包 | 新终端先source /opt/ros/noetic/setup.bash和~/vnav_ws/devel/setup.bash |
| Unity打开，但无人机不飞 | 检查控制器是否补全、是否运行、话题是否有数据 |
| 一启动就翻或乱转 | 停控制器；优先查坐标系、单位和分配矩阵，不盲目加大参数 |
| 网页Temporary failure resolving | 网络/DNS问题，发命令输出；不要把它当代码问题 |

## 十三、最后统一发我什么

你身份信息已经收到，不用重复发。统一发送：截图01—10、最终controller_pkg压缩包、完整绕圆视频或链接、最终四个增益、实际调参记录；有bag也一起发。老师模板若有就附上。

我会据真实材料整理理论题和最终实验报告。有bag可计算误差，没有bag就写定性结果，不能由单张截图编造RMSE。

## 十四、GitHub放什么

本指南适合放个人仓库的lab3/Lab3_操作与截图回传指南.md。个人理论题也放个人仓库lab3。团队完整controller_pkg和rviz_drone_flight.txt按老师指定团队仓库提交；个人仓库中的指南不能替代团队提交。

不要上传build、devel、logs或很大的仿真器文件。视频按题面放外部平台，仓库只放链接；bag保留作分析材料，不直接塞进普通Git提交。

## 参考资料

- 2023官方题面：https://vnav.mit.edu/labs_2023/lab3/exercises.html
- 你使用的源码版本：https://github.com/MIT-SPARK/VNAV-labs/releases/tag/VNAV2021
- 仿真器下载：https://vnav.mit.edu/material/lab3.zip
- 几何控制参考：Lee等，Geometric tracking control of a quadrotor UAV on SE (3)，CDC 2010。

