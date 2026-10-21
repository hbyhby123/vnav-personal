# Lab 3 小白操作与检查复习指南

> 最新悬停记录：kx=2、kv=3、kr=3、komega=1；用户反馈不再晃动，单次高度1.957025米。接下来测试圆轨迹，尚未确认绕圆成功。

适用：Ubuntu 20.04.6、ROS Noetic、VNAV2021源码。更新日期：2026年10月21日。

## 一、先看你现在做到哪了

| 事情 | 目前状态 |
|---|---|
| Ubuntu和ROS环境 | 已确认符合要求 |
| 下载实验代码、安装依赖 | 已完成 |
| 编译8个ROS包 | 已成功 |
| 下载TESSE仿真器lab3.zip | 已完成 |
| 启动仿真器、桥接、RViz | 已成功启动过；全部关闭后的重开方法见第8步 |
| 补全控制器、悬停和绕圆 | 已安装并实现悬停；接下来执行第8步测试绕圆 |
| 理论题、视频和最终报告 | 后续完成 |

当前控制器已补全并安装；悬停阶段已收到实际高度读数。圆轨迹仍需单独测试，不能把悬停成功当作绕圆完成。

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

截图03：TESSE仿真器初始场景。现在无人机不飞很正常，控制器尚未安装或启动时不会受控飞行。

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

## 六、控制器已补好：下载替换并编译

详细小白教程：[第六步：补全控制器与悬停操作](06_补全控制器与悬停操作.md)。已提供对应VNAV2021的完整控制器实现，你已完成安装与悬停。本节留作以后重装参考，现在直接看第8步。

若旧控制器正在运行，先在它的终端按Ctrl+C。然后新开Ubuntu终端：

```bash
mkdir -p ~/lab3_evidence
wget -O ~/lab3_evidence/install_controller.sh https://raw.githubusercontent.com/hbyhby123/vnav-personal/master/lab3/scripts/install_controller.sh
```

只有下载成功后才运行：

```bash
bash ~/lab3_evidence/install_controller.sh
source ~/vnav_ws/devel/setup.bash
```

脚本会备份原包、替换3个文件并编译。Summary全部成功后截05。默认已设为悬停模式；接着按第七节启动，不用重复改STATIC_POSE。初始增益kx=2、kv=3、kr=3、komega=1，需要实际飞行确认。运行脚本会把轨迹模式重设为悬停，因此不要在完成调参和绕圆后无故重复安装。

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
roslaunch controller_pkg traj_tracking.launch kx:=2 kv:=3 kr:=3 komega:=1
```

代码补全后，目标是飞到(0,0,2)米附近并保持，期望yaw为45度。观察约20—30秒，截图06。这个观察时长是建议，不是官方评分阈值。

### 第8步：切换绕圆（所有终端都关了也从这里做）

目前已完成：悬停不再明显晃动，单次实际位置读数为x=0、y=0、z=1.957025米。采用kx=2、kv=3、kr=3、komega=1。这里只能说明该次悬停观察，不能当作圆轨迹已成功。

**需要打开4个终端：A开Unity，B开桥接，C开RViz，D修改/编译/启动控制器。** 已经打开的程序不要重复启动；如果全关了，就逐个执行下面步骤。

**① 终端A：打开仿真器**

```bash
cd ~/vnav-builds/lab3
./lab3.x86_64
```

出现无人机场景后保持运行。

**② 新开终端B：打开桥接**

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch
```

保持运行。桥接负责在仿真器和控制器之间传数据。

**③ 新开终端C：打开RViz**

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roscd controller_pkg
rviz -d rviz/lab3.rviz
```

保持运行，后续用它观察和录制绕圆。

**④ 新开终端D：把悬停模式改成圆轨迹**

如果旧控制器还在运行，先在它的终端按Ctrl+C；全关过则无需再停。执行：

```bash
gedit ~/vnav_ws/src/controller_pkg/src/traj_publisher.cpp
```

找到顶部这一行：

```cpp
#define STATIC_POSE 1
```

只把1改成0，保存并关闭编辑器：

```cpp
#define STATIC_POSE 0
```

若已经是0，不必再改。0表示圆轨迹，1表示定点悬停。

**⑤ 在终端D编译**

```bash
source /opt/ros/noetic/setup.bash
cd ~/vnav_ws
catkin build
source ~/vnav_ws/devel/setup.bash
```

只有Summary全部成功才继续。缺截图05时，可在此补截编译成功摘要。

**⑥ 重置并用当前稳定参数启动**

点击Unity画面，按R重置。然后回到终端D执行：

```bash
roslaunch controller_pkg traj_tracking.launch kx:=2 kv:=3 kr:=3 komega:=1
```

明确写四个参数，可避免Ubuntu本地旧launch默认值影响结果。不用重新运行安装脚本，否则会把轨迹模式改回悬停。

**⑦ 观察结果**

初始切入圆轨迹时可能动作较快。先观察能否持续绕圆；若明显翻转或振荡越来越大，在终端D按Ctrl+C停止，保持另外三个窗口打开，把现象发给我。

悬停稳定的参数未必能直接满足圆轨迹，若无法跟踪需要根据实际结果继续调参。稳定完成一圈后，保存：

- 07_RViz俯视视角下无人机圆轨迹跟踪与期望轨迹对比.png
- 08_RViz三维视角下无人机圆轨迹跟踪与飞行高度展示.png

再按第9—11步检查话题、录制视频和bag。截图不能替代完整一圈的视频。

原始代码给定的轨迹：半径5米、高度2米、一圈约12.6秒，yaw随时间变化。默认先保留这些轨迹参数，暂不同时修改半径或速度。

### 调参怎么记

参数文件：~/vnav_ws/src/controller_pkg/launch/traj_tracking.launch。

| 参数 | 通俗含义 |
|---|---|
| kx | 偏离目标位置时，拉回去的力度 |
| kv | 速度误差反馈，也帮助抑制平移振荡 |
| kr | 机身姿态偏离目标时，纠正的力度 |
| komega | 旋转速度误差反馈，也帮助抑制转动振荡 |

原始版本四个值都是1；本次实现的初始值为kx=2、kv=3、kr=3、komega=1，不能保证在实际仿真中已经合适。先检查公式、坐标和转子顺序，再调增益。一次只改一项，记录“旧值、新值、现象”。仅修改launch参数时，保存并重启终端D即可；修改C++后才需要重新编译。

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
| 06B | 06B_定点悬停实际位置与1.957米高度验证.png | 终端中的实际位置读数，z约1.957米 |
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
