# VNAV 课程实验

黄博宇 · 24020036026 · 中外计科一班 · 第8组

这里按 Lab1—Lab5 保存报告、源码和实际运行记录。先在下表找到实验，再打开该实验的 README 查看环境、操作和结果。

## 实验导航

| 实验 | 学什么 | 中文报告 | English report | 代码 | 截图与数据 |
| --- | --- | --- | --- | --- | --- |
| [Lab1](lab1/README.md) | 开发工具与C++基础 | [中文 PDF](lab1/report/Lab1_实验报告_黄博宇_完整版.pdf) | [English PDF](lab1/report/Lab1_Report_EN.pdf) | [代码](lab1/lab1_demo/) | [证据](lab1/report/figures/) |
| [Lab2](lab2/README.md) | ROS与坐标变换 | [中文 PDF](lab2/Lab2_Report_CN.pdf) | [English PDF](lab2/Lab2_Report_EN.pdf) | [代码](lab2/two_drones_pkg/) | [证据](lab2/images/) |
| [Lab3](lab3/README.md) | 无人机轨迹控制 | [中文 PDF](lab3/deliverables/Lab3_Report_CN_Huang_Boyu.pdf) | [English PDF](lab3/deliverables/Lab3_Report_EN_Huang_Boyu.pdf) | [代码](lab3/code/README.md) | [证据](lab3/data/README.md) |
| [Lab4](lab4/README.md) | 无人机控制与竞速 | [中文 PDF](lab4/deliverables/Lab4_实验报告_黄博宇.pdf) | [English PDF](lab4/deliverables/Lab4_Report_EN_Boyu_Huang.pdf) | [代码](lab4/code/README.md) | [证据](lab4/data/README.md) |
| [Lab5](lab5/README.md) | 无人机视觉跟踪 | [中文 PDF](lab5/deliverables/LAB5_无人机视觉跟踪实验报告.pdf) | [English PDF](lab5/deliverables/LAB5_Visual_Tracking_Report_EN.pdf) | [代码](lab5/feature_tracking/README.md) | [证据](lab5/screenshots/README.md) |

## 按目的查找

- **看报告或交作业**：先用上表的中英文 PDF 入口，再核对各 Lab 的交付要求。
- **运行程序**：打开对应 Lab 的 README，使用该实验记录的系统、依赖和参数。
- **检查实验是否真的跑过**：结合截图、视频、bag、逐帧 CSV 和分析说明，不只看一张结果图。
- **复习或演示**：[阅读与复现路线](docs/阅读与复现路线.md)列出建议顺序。
- **维护仓库**：看[目录与文件规范](docs/目录与文件规范.md)和[提交说明](CONTRIBUTING.md)。

## 目录结构

```text
.
├── README.md          五个实验的总入口
├── docs/              报告索引、阅读路线和文件规范
├── tools/             仓库导航检查工具
├── CONTRIBUTING.md    怎样整理文件、怎样写清楚提交备注
├── CHANGELOG.md       用通俗语言记录主要更新
├── lab1/              Linux、Git、C++和CMake基础
├── lab2/              ROS、TF与相对轨迹
├── lab3/              悬停和圆轨迹跟踪
├── lab4/              轨迹规划与穿门竞速
└── lab5/              特征匹配、稀疏跟踪与稠密光流
```

各 Lab 的运行目录沿用原项目路径。报告、代码、原始证据和派生分析的对应关系，统一写在[完整资料索引](docs/报告与证据索引.md)中。

## 环境怎么选

| 实验 | 主要工具 | 一句话说明 |
| --- | --- | --- |
| Lab1 | Linux、Git、GCC、CMake | 学会组织源码并编译程序 |
| Lab2 | ROS、TF、RViz | 用消息和坐标关系描述相对运动 |
| Lab3 | ROS Noetic、TESSE、几何控制器 | 根据目标和反馈控制旋翼 |
| Lab4 | ROS Noetic、TESSE Lab4、轨迹优化库 | 规划并跟踪穿过多个赛门的路线 |
| Lab5 | ROS Noetic、OpenCV 4.2 contrib | 从相邻图像中建立和验证对应关系 |

```bash
git clone https://github.com/hbyhby123/vnav-personal.git
cd vnav-personal
# 接着打开对应 lab*/README.md，按该实验的命令操作。
```

只想查看一个实验时，可使用[按需下载方法](docs/阅读与复现路线.md#只下载需要的实验)。

## 最新整理

Lab5 已归档中英文各19页报告、17张编号截图、7张流程或统计图以及完整逐帧记录；每份报告含24幅图和11张表。五个实验的报告与代码入口已统一。

更多更新见[更新记录](CHANGELOG.md)。仓库归档与课程正式提交是不同环节；具体交付状态以各 Lab 的说明和作业平台记录为准。
