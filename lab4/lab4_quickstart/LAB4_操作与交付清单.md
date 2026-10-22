# LAB4 从现有Lab3到完整竞速：操作、截图与检查演示

更新：2026年10月21日。适用：Ubuntu 20.04.6、ROS Noetic、VNAV2021。

## 先认清你现在做到哪里

已根据你在Lab3聊天中的最新反馈更新：你已经完成控制器，定点悬停稳定，圆轨迹基本不晃；增益是 **kx=2、kv=3、kr=3、komega=1**。某次悬停高度1.957025米仅是一次读数。

**所以：不用重装ROS，不用重新做Lab3，不要用官方空白controller覆盖你已经调好的代码。** Lab4沿用现有controller_pkg和bridge。以前“src为空”的记录已过时。

随文提供`lab4_quickstart.zip`：Lab4四个Part的代码补丁、安装脚本、模拟器路径识别脚本、同时录像和录bag的脚本。代码已按官方VNAV2021框架补齐，并做本地静态检查；尚未在你的Ubuntu上编译或完成飞行验证。遇到错误，把日志发来继续修正。

## 1. 任务和交付物，先看这一张表

| 项目 | 要做什么 | 必须交付什么 |
|---|---|---|
| 个人题1，20分 | 单段最小速度轨迹：一次、二次、三次；加入终点速度约束后再求解 | 排版后的推导PDF：QP矩阵、最优系数、轨迹、代价、比较 |
| 个人题2，15分 | k段最小snap的次数与约束计数，推广到r阶 | 排版后的推导PDF：假设、未知量、约束分类与数量 |
| 团队竞速，65分 | Part0首门悬停；Part1.1状态读取；Part1.2轨迹优化；Part1.3轨迹跟随 | 改后源码、完整通关视频、最快完整一轮bag、rviz_drone_race.txt中的两个公开链接 |
| 可选加速 | 完整通关后提高速度 | 有效轮次的时间和参数对比；加分规则以本校要求为准 |

截图用于写报告，不能代替视频、bag和源码。理论题可以等你飞行时同步处理，不用先做完再开模拟器。

### 当前进度：20个包全部编译成功

用户回传的编译摘要：All 20 packages succeeded、3个包有警告、无失败。请保留截图：`02_Lab4环境依赖修复后20个ROS包全部编译成功.png`。

警告中的%d和size_type是日志格式不匹配，不影响本次构建；仓库补丁已使用显式int转换。这个警告也提示当前Ubuntu可能仍在编译原始框架，编译成功不代表Part空白已补齐。继续前先检查两个源码中的FILL IN HERE；若仍有空白，按A3安装补丁后重新编译，再进行B首门测试。

## 2. 最快操作顺序

**备份Lab3 → 安装Lab4代码 → 下载Lab4模拟器 → 首门悬停 → 完整竞速 → 同时保存录像和bag → 发材料给我写报告。**

下面只需首次做A；以后给助教演示直接看F。

## A. 首次准备Lab4：沿用已经完成的Lab3

### A1. 停掉Lab3控制器并备份

在原来运行`traj_tracking.launch`的终端按Ctrl+C。关闭原来的Unity Lab3窗口和旧桥接，确保没有旧控制器在发命令。

新开Ubuntu终端：

```bash
source /opt/ros/noetic/setup.bash
mkdir -p ~/lab4_evidence/{screenshots,logs,runs,backups}
tar -czf ~/lab4_evidence/backups/controller_pkg_before_lab4_$(date +%Y%m%d_%H%M%S).tar.gz -C ~/vnav_ws/src controller_pkg
ls ~/vnav_ws/src
lsb_release -d
rosversion -d
```

**成功标志：**还能看到controller_pkg、bridge等Lab3已有包，备份文件已生成。

**截图01：`01_Lab4准备_Ubuntu20.04_ROSNoetic_Lab3控制器备份与现有工作空间目录.png`**

### A2. 把附件包放到Ubuntu，解压

下载本聊天提供的`lab4_quickstart.zip`，通过浏览器、共享文件夹或拖放传到Ubuntu的“下载”目录。

先确认它在哪里：

```bash
find ~/Downloads ~/下载 ~/Desktop -maxdepth 2 -name lab4_quickstart.zip 2>/dev/null
```

下面假设输出是`/home/by/Downloads/lab4_quickstart.zip`。如果不同，把第二条命令里的路径换成find找到的路径：

```bash
sudo apt install -y unzip ffmpeg x11-utils
unzip -n ~/Downloads/lab4_quickstart.zip -d ~/
ls ~/lab4_quickstart/scripts
```

如果已解压过旧版本，先把旧的`~/lab4_quickstart`改名保存，再解压新版。

### A3. 一条命令安装Lab4并编译

```bash
bash ~/lab4_quickstart/scripts/install_lab4.sh
```

脚本会：

1. 检查现有Lab3控制器是否存在，保留它。
2. 有`~/labs/lab4`就使用；没有`~/labs`时下载官方VNAV2021。
3. 把Lab4的包和依赖补进工作空间，备份已有Lab4文件。
4. 若Lab4依赖已包含mav_msgs，把Lab3单独克隆的mav_comm移到备份目录，避免重复包名。
5. 安装补好的两个C++和三个launch，再运行catkin build。

**不要再执行`cp -r ~/labs/lab3/. ~/vnav_ws/src/`，它会覆盖你做好的Lab3。**

完成后：

```bash
source ~/vnav_ws/devel/setup.bash
rospack find controller_pkg
rospack find planner_pkg
rospack find trajectory_generation
rospack find tesse_ros_bridge
```

**成功标志：**构建摘要无失败包，四个包能定位。包数量会随工作空间不同，不要求某个固定数字。

**截图02：`02_Lab4补全代码安装后catkin_build成功摘要与四个ROS包定位.png`**

失败则发`~/lab4_evidence/logs/build_日期时间.txt`全文。不要反复重装控制器。

### A4. 下载Lab4模拟器

GitHub源码不是模拟器。先下载Lab4场景：

```bash
mkdir -p ~/vnav-builds
cd ~/vnav-builds
wget -c https://vnav.mit.edu/material/lab4.zip
unzip -n lab4.zip
```

历史链接若失败，使用[官方README提供的模拟器目录](https://drive.google.com/drive/folders/1Bwu1lw9qx_TdibhPuYPpDLbJaBEBvBRb?usp=sharing)，下载Lab4的Linux版本并解压到`~/vnav-builds`。不要下载Lab3场景代替。

识别实际路径：

```bash
python3 ~/lab4_quickstart/scripts/find_simulator.py
```

**成功标志：**输出SIM_EXEC、SIM_DATA，并保存到`~/lab4_evidence/sim.env`。脚本根据赛门CSV定位，不强行要求解压目录名。

若找到0个或多个模拟器，把输出发给我。官方航点读取器要求文件`StreamingAssets/vnav-2020-lab4_static_tfs.csv`存在；只有x86_64文件不够。

**截图03：`03_Lab4模拟器路径确认_可执行文件与赛门CSV数据目录.png`**

## B. 首门悬停：确认Lab3控制器能接上Lab4

需要4个终端，每个按Ctrl+Alt+T新开。前三个保持运行。

### 终端1：打开Lab4模拟器

```bash
source ~/lab4_evidence/sim.env
cd "$(dirname "$SIM_EXEC")"
"$SIM_EXEC"
```

出现竞速赛道后，点击Unity按R复位。

**截图04：`04_Unity_Lab4竞速场景_无人机起点与赛门分布.png`**

### 终端2：打开ROS桥接

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roslaunch tesse_ros_bridge tesse_quadrotor_bridge.launch
```

桥接的作用是传回实际状态、发出旋翼命令。

### 终端3：启动首门悬停

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
source ~/lab4_evidence/sim.env
roslaunch planner_pkg static_point_test.launch simulator_data_directory:="$SIM_DATA" kx:=2 kv:=3 kr:=3 komega:=1
```

**成功标志：**无人机飞到第一道门的位置并稳定保持。先观察10秒，实际不稳定就记录问题，不要写成成功。

**截图05：`05_Part0首门悬停成功_无人机在第一道赛门中心附近稳定保持.png`**

### 终端4：检查期望和实际状态

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
rostopic echo -n 1 /desired_state
rostopic echo -n 1 /current_state
rosparam get /kx
rosparam get /kv
rosparam get /kr
rosparam get /komega
```

对比期望位置和实际位置；无需把零点几米误差直接判为失败，先看是否收敛、是否持续振荡。增益应为2、3、3、1。

**截图06：`06_首门悬停验证_期望与实际三维位置及四个控制器增益.png`**

一张放不下时拆06a、06b。截图名对应实际内容即可。

### 结束首门测试

在终端3按Ctrl+C关闭悬停测试。不要启动Lab3的traj_tracking.launch，它会再发一套目标并启动另一个控制器。

## C. 完整竞速：先跑通，再追求速度

### C1. 保留终端1和2，在终端3启动轨迹跟随

点击Unity按R复位，再运行：

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roslaunch trajectory_generation traj_following.launch kx:=2 kv:=3 kr:=3 komega:=1 time_scale:=2.0
```

此时还没发赛门，不会开始完整轨迹。出现等待状态提示时，先确认bridge有数据。

这里time_scale=2.0表示把原估计段时间乘2，以较慢速度做第一次测试；不是官方规定值。50Hz期望状态发布也是本补丁的设置，官方框架原来是5Hz。

### C2. 终端4：开启命令行录像和飞行数据记录

```bash
bash ~/lab4_quickstart/scripts/record_race.sh
```

看到“Video and bag recording”后，才进入C3。此终端保持打开。

脚本会记录Ubuntu桌面视频、状态bag、参数、关键源码和日志。录像开始前有5秒准备时间；摆好Unity和RViz窗口后不要改变桌面分辨率。

### C3. 终端5：最后发布赛门，开始飞

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
source ~/lab4_evidence/sim.env
roslaunch planner_pkg traj_gen.launch simulator_data_directory:="$SIM_DATA"
```

随后切回Unity看飞行。**必须按“跟随器→记录→航点”顺序，否则可能漏录起飞。**

**截图07：`07_Lab4航点读取与轨迹优化成功_赛门数量和轨迹进度日志.png`**

**截图08：`08_Lab4竞速过程_无人机穿越中间赛门画面.png`**

**截图09：`09_Lab4完整通关_无人机通过最后一道赛门后的画面.png`**

08、09可从完整视频截取，记下视频时间。视频要连续覆盖全部赛门；单张终点截图不能证明完整通关。

### C4. 结束录制并检查

最后一门通过后等3秒，回终端4按Enter，等脚本输出Saved路径。它会正常结束ffmpeg和rosbag，不要直接关虚拟机。

```bash
ls -lt ~/lab4_evidence/runs
```

每轮自动建一个`run_日期时间`文件夹，里面包含：

| 文件 | 用途 |
|---|---|
| race.mp4 | 桌面上的完整竞速视频 |
| race.bag | 实际状态、期望状态、航点、旋翼命令和clock（实际存在的消息） |
| parameters.yaml | 本轮所有ROS参数 |
| bag_info.txt | 时长、消息数、话题信息 |
| 两个cpp与traj_following.launch | 本轮关键代码快照 |
| rosbag.log / ffmpeg.log | 录制错误排查 |
| desired_state_publishers.txt | 检查有没有多余的目标发布者 |

查看和播放：

```bash
xdg-open ~/lab4_evidence/runs
```

双击最新轮次的race.mp4，确认清晰、无黑屏、完整穿过所有门；打开bag_info.txt，确认有/current_state和/desired_state且消息数不为0，bag覆盖全程。

**截图10：`10_最快完整竞速bag检查_文件名_持续时间_实际与期望状态话题及消息数.png`**

正式最快轮次确定后，再用那一轮信息截图。失败轮也会保存文件，文件存在不代表通关。

### C5. 录像失败时的单独录bag命令

先按Ctrl+C退出失败的录制脚本，再在触发航点前运行：

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
rosbag record -O ~/lab4_evidence/runs/manual_$(date +%Y%m%d_%H%M%S).bag /current_state /desired_state
```

完整通关后在此终端按Ctrl+C，等待写完。录像仍需补录同一轮。X11录屏提示Wayland时，退出Ubuntu账户，在登录界面的齿轮里选择“Ubuntu on Xorg”再登录。

### C6. 再跑一轮和提速

1. 终端5按Ctrl+C停航点。
2. 终端3按Ctrl+C停跟随器和控制器。
3. Unity按R复位。
4. 从C1重新启动；每轮重新运行录制脚本。

不能只按R接着跑：旧节点可能保留轨迹和起始时间。

先争取time_scale=2.0完整通过。成功后可试1.5，再试1.0；不要同时更改控制器增益。原时间估计仍可能太快或出现切弯漏门，需以实际飞行调整。更小时间倍率不保证更好的有效成绩。

| 轮次 | time_scale | 控制增益 | 全部门通过？ | 视频计时起止点 | 用时 | 问题 |
|---|---|---|---|---|---|---|
| run_日期时间 | 2.0 | 2/3/3/1 | 待填 | 待填 | 待填 | 待填 |

计时统一用“开始执行竞速轨迹→通过最后一门”的视频时间戳。bag总时长含准备和结束阶段，不能直接当成绩。只比较完整通过的轮次。

## D. RViz怎么打开，截图能不能少一点

如果需要展示实际和期望位姿，额外开终端：

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
roscd controller_pkg
rviz -d rviz/lab3.rviz
```

Part0补丁沿用world→desired_pose目标TF。竞速节点主要发/desired_state，不保证旧Lab3 RViz配置自动画出整条优化轨迹。如果只看到实际位姿，不要称为期望与实际轨迹对比；可先完成Unity视频和bag，再据数据生成报告轨迹图。

**可以精简截图：**05保留一张清晰首门悬停；08保留一张中途穿门；09保留一张终点即可，不用每道门都截。完整性用视频证明。

截图11可选：`11_可选_RViz展示无人机实际位姿与参考坐标系.png`。

截图12可选：`12_可选_加速前后完整通关时间与轨迹时间倍率对比.png`。

## E. 故障时先看这张表

### NLopt下载连接被拒绝

历史故障：13/21包成功时nlopt下载失败；用户随后反馈修复后20个包全部编译成功。以下脚本仅供该故障复现时使用，不需要在成功后重复运行：

```bash
bash ~/lab4_quickstart/scripts/repair_nlopt.sh
```

脚本从已核对的原始归档直连下载NLopt 2.4.2，校验SHA256（检查下载内容是否一致），再让构建读取本地归档。下载地址在当前机器验证可用，用户Ubuntu的编译结果仍需回传确认。


### 已出现的配置问题：2026年10月22日更新

如果出现 `gflags_catkin` 无法解析，同时 `catkin_simple` 仍指向旧的 `src/catkin_simple`：这是缺少源码依赖，以及依赖搬到dependencies后留下的旧构建缓存。新版快速包已补上gflags_catkin并在安装时备份旧build/devel后重建。

已有工程可运行新版包内修复脚本：

```bash
bash ~/lab4_quickstart/scripts/repair_dependencies.sh
```

脚本不改src中的实验代码；旧build/devel移到lab4_evidence/backups中保留，重新构建。日志保存在lab4_evidence/logs/repair_日期时间.txt。失败轮次尚未执行模拟器下载，修复编译后继续A4。

| 问题 | 先做什么 | 发给我什么 |
|---|---|---|
| catkin报同名包 | 不再克隆mav_comm；检查旧独立版本是否已移到备份 | 完整编译日志和重复包路径 |
| controller_pkg找不到 | source工作空间；确认Lab3包仍在 | rospack输出、src列表 |
| 无法打开赛门CSV | 重跑find_simulator.py；launch传入SIM_DATA | sim.env、CSV查找结果、报错 |
| 一启动就翻倒 | 先停跟随器，再按R；确认没有旧Lab3控制器 | 节点列表、增益、状态和视频 |
| 没有轨迹或不动 | 确认先有/current_state，再运行航点发布 | 下方检查命令输出 |
| 漏门、碰撞、振荡 | 保留本轮数据；下一轮用更慢time_scale | bag、参数、对应视频 |
| 录像黑屏或退出 | 确认Xorg、桌面分辨率没变 | ffmpeg.log、终端输出 |

通用检查命令（另开终端）：

```bash
source /opt/ros/noetic/setup.bash
source ~/vnav_ws/devel/setup.bash
rosnode list
rostopic info /desired_state
rostopic echo -n 1 /current_state
rostopic echo -n 1 /desired_traj_vertices
rostopic hz /desired_state
```

hz观察几秒后Ctrl+C。可以发文字，不必为了每次排查额外截图。

## F. 以后给助教检查演示：完整启动顺序

安装和编译已经成功、代码没再改时，直接按顺序开5个终端：

1. 按B的终端1命令打开Lab4 Unity，按R复位。
2. 按B的终端2命令打开bridge。
3. 需要先演示悬停时运行B的终端3，完成后Ctrl+C关闭。
4. 按C1启动竞速跟随器，使用已经验证成功的time_scale和增益。
5. 按C2开启录制。
6. 按C3发布航点，展示完整通关。
7. 通关后回录制终端按Enter，等待保存完成。

每次演示无需重新下载、安装或编译；只有改过C++才需要catkin build。

助教问时可以这样解释：

| 问题 | 简单回答 |
|---|---|
| Lab3和Lab4有什么关系 | Lab3负责根据目标算旋翼转速，Lab4负责规划飞过赛门的目标轨迹 |
| 赛门从哪里来 | 读取模拟器静态CSV，转换到ROS坐标，再发布PoseArray |
| 为什么要处理yaw | 朝向跨±π时直接插值可能绕一大圈，需要展开为连续角度 |
| 为什么先悬停 | 先验证控制器、坐标和通信，再排查轨迹跟随 |
| 为什么重跑要重启节点 | 节点会保留已有轨迹，需要重新设起点和计时 |
| 怎么判断完成 | 连续视频显示依次通过全部赛门，bag保留同轮实际与期望状态 |
| 代码里N=10是什么 | 每段10个系数，最高九次；不是理论题中直接推出的次数 |

## G. 截图编号与详细文件名总表

| 编号 | 保存文件名 | 何时截 |
|---|---|---|
| 01 | 01_Lab4准备_Ubuntu20.04_ROSNoetic_Lab3控制器备份与现有工作空间目录.png | A1 |
| 02 | 02_Lab4补全代码安装后catkin_build成功摘要与四个ROS包定位.png | A3 |
| 03 | 03_Lab4模拟器路径确认_可执行文件与赛门CSV数据目录.png | A4 |
| 04 | 04_Unity_Lab4竞速场景_无人机起点与赛门分布.png | B终端1 |
| 05 | 05_Part0首门悬停成功_无人机在第一道赛门中心附近稳定保持.png | 稳定悬停时 |
| 06 | 06_首门悬停验证_期望与实际三维位置及四个控制器增益.png | B终端4 |
| 07 | 07_Lab4航点读取与轨迹优化成功_赛门数量和轨迹进度日志.png | C3 |
| 08 | 08_Lab4竞速过程_无人机穿越中间赛门画面.png | 完整视频中 |
| 09 | 09_Lab4完整通关_无人机通过最后一道赛门后的画面.png | 同轮视频末段 |
| 10 | 10_最快完整竞速bag检查_文件名_持续时间_实际与期望状态话题及消息数.png | C4 |
| 11可选 | 11_可选_RViz展示无人机实际位姿与参考坐标系.png | 需要RViz展示时 |
| 12可选 | 12_可选_加速前后完整通关时间与轨迹时间倍率对比.png | 做了有效加速对比时 |

代码截图不强制额外拍四张；回传完整源码后，我可摘取关键代码写报告。图名应与图中事实相符，失败时不要保存成“成功”。

## H. 理论题与最终报告材料

个人题1完整覆盖：J=∫₀¹[P′(t)]²dt，P(0)=0、P(1)=1；一次最优解和代价；二次与三次的Q、A、b、最优解和代价；Euler–Lagrange比较；新增P′(1)=-2后分别求二次与三次解及代价。

个人题2完整覆盖：固定段时间、一维情形，k段、r=4时的多项式次数与未知数；waypoint/free derivative/fixed derivative分类、每类产生多少方程；推广到任意r、k。要区分显式约束和最优性产生的自然连接条件。

理论尚未做可以直接告诉我，我可协助推导、核验并排版PDF，不需要你先制造结果截图。

**第一次回传：**安装编译日志、模拟器路径识别结果、首门悬停是否成功及截图05/06。

**完成后回传：**

- 截图01～10；11/12可选。
- 最快完整一轮整个run文件夹，包含mp4、bag、参数和代码；大文件可给可下载链接。
- 最终完整controller_pkg、planner_pkg、trajectory_generation_pkg，特别是你后来改动过的文件。
- 运行表：完整成功与失败轮次、参数、视频起止时间、用时、问题和解决方法。
- 姓名学号、成员分工、实验日期、教师报告模板。
- 理论题已有推导，或注明需要我协助推导。

打包源码（在停止本轮录制后执行）：

```bash
tar -czf ~/lab4_evidence/lab4_final_code_$(date +%Y%m%d_%H%M%S).tar.gz -C ~/vnav_ws/src controller_pkg planner_pkg trajectory_generation_pkg
```

如果需要轨迹误差图和RMSE，要有bag；截图无法可靠计算。最终报告据实写结果，不把尚未验证的代码或理想仿真当实测。

## I. 正式提交清单

仓库建立lab4文件夹，提交理论PDF/综合报告PDF、修改后的源码和启动说明。个人理论按个人仓库提交，团队部分按教师规定团队仓库提交。

把完整视频和最快完整bag上传Google Drive或Dropbox，设为持链接者可访问，用未登录窗口测试。`rviz_drone_race.txt`写：

```text
Video: <完整通关视频公开链接>
Rosbag: <最快完整一轮bag公开链接>
Run ID: <与本地run目录一致>
Race time: <用时和计时起止定义>
Parameters: kx=2, kv=3, kr=3, komega=1, time_scale=<实际值>
Code version: <最终版本>
```

当前代码和操作资料归档于[GitHub Lab4目录](https://github.com/hbyhby123/vnav-personal/tree/master/lab4)。安装脚本不自动上传实验视频、bag或正式提交，实验完成后再提交真实结果。

## 依据

- [MIT Lab4要求](https://vnav.mit.edu/labs_2023/lab4/exercises.html)
- [VNAV2021实验代码](https://github.com/MIT-SPARK/VNAV-labs/releases/tag/VNAV2021)
- [Lab4原始轨迹节点](https://github.com/MIT-SPARK/VNAV-labs/blob/VNAV2021/lab4/trajectory_generation_pkg/src/trajectory_generation_node.cpp)
- [Lab4原始航点读取器](https://github.com/MIT-SPARK/VNAV-labs/blob/VNAV2021/lab4/planner_pkg/src/traj_vertices_publisher.cpp)
- 你在“总结 Lab 3 任务与交付”中的最新实验反馈，以及该聊天保存的从零准备到检查演示文档。
