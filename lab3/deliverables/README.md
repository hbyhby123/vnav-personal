# 正式交付材料

**本次只提交：[英文完善版报告](Lab3_Report_EN_Huang_Boyu.pdf)。D2也已改为英文版。整包下载见[最终提交入口](../submission/README.md)。中文版也已更新为20页，供阅读复习；最终提交仍使用英文版。**

PDF是固定排版文件，便于提交；Markdown是可以直接修改的纯文字文档，图片通过相对路径引用。

## 名词说明

| **术语** | **大白话解释** |
| --- | --- |
| ROS | 让多个程序通过消息协作的软件框架 |
| 四元数 | 用4个数表示三维方向的方法 |
| Eigen | C++中用于向量和矩阵计算的库 |
| 矩阵秩 | 一组关系中真正独立的关系数量 |
| yaw | 机身在水平方向的转向角 |
| bag | 按时间保存ROS消息的记录文件 |
| PDF | 固定排版文档格式 |
| Markdown | 可直接编辑、可以通过链接引用图片的纯文字格式 |

## 任务内容

| **任务名称** | **要解决的问题** | **采用的方法 / 技术** | **预期结果** |
| --- | --- | --- | --- |
| 个人D1 | 完成旋转表示转换五问 | ROS四元数与Eigen矩阵接口；Eigen是C++矩阵计算库 | 可阅读的文本答案 |
| 个人D2 | 解释控制能力与阻力补偿 | 分配矩阵秩分析和动力学推导；秩表示独立控制关系的数量 | 2页推导PDF |
| 综合报告 | 把方法和真实结果说明白 | 文字、原始截图与bag统计 | 20页英文报告及可编辑原稿 |

## 交付文件

| **文件 / 目录** | **作用** | **说明** |
| --- | --- | --- |
| [Lab3_Report_CN_Huang_Boyu.pdf](Lab3_Report_CN_Huang_Boyu.pdf) | 20页中文全截图版 | 阅读与复习，不放入英文提交包 |
| [Lab3_Report_CN_Huang_Boyu.md](Lab3_Report_CN_Huang_Boyu.md) | 中文可编辑原稿 | 引用assets_current |
| [Lab3_Report_EN_Huang_Boyu.pdf](Lab3_Report_EN_Huang_Boyu.pdf) | 20页英文完善版 | 本次提交报告 |
| [Lab3_Report_EN_Huang_Boyu.md](Lab3_Report_EN_Huang_Boyu.md) | 英文可编辑原稿 | 引用assets_current |
| [deliverable_2_English.md](deliverable_2_English.md) | D2英文原稿 | 对应最新deliverable_2.pdf |
| [assets_current/](assets_current/README.md) | 当前中英文稿的图片 | 新版素材 |
| [assets/](assets/README.md) | 可编辑报告需要的图片素材 | 进入下层查看逐文件清单 |
| [Lab3_实验报告_可编辑原稿.md](Lab3_实验报告_可编辑原稿.md) | 可编辑报告文本，引用assets及data中的图片 | 现有文件 |
| [Lab3_实验报告_黄博宇.pdf](Lab3_实验报告_黄博宇.pdf) | 旧中文报告，仅留档；本次不提交 | 现有文件 |
| [README.md](README.md) | 本层任务、文件、输入输出、参数和原理说明 | 说明文件 |
| [deliverable_1.txt](deliverable_1.txt) | 个人D1五问答案，含四元数转换代码 | 现有文件 |
| [deliverable_2.pdf](deliverable_2.pdf) | 个人D2两问的2页英文推导 | 现有文件 |

## 核心代码 / 函数

| **函数名 / 代码 / 配置** | **作用** | **通俗说明** |
| --- | --- | --- |
| — | 本目录没有运行代码 | 报告说明代码，真正可运行包在../code/controller_pkg |
| deliverable_1.txt | D1答案 | 四元数互转、标量、yaw、Eigen矩阵 |
| deliverable_2.pdf | D2答案 | 结构失秩与阻力补偿推导 |

## 输入 / 输出

| **输入** | **输出** | **格式 / 示例** |
| --- | --- | --- |
| 源码、截图、bag计算结果 | 正式报告与理论题答案 | PDF / TXT / Markdown |
| 可编辑报告中的图片引用 | assets与../data中图片 | 修改目录时需同步相对链接 |

## 参数说明

| **参数** | **含义** | **默认值** |
| --- | --- | --- |
| 学生 / 组号 | 报告署名 | 黄博宇 / 第8组 |
| 最终增益 | 报告对应的真实运行参数 | 2 / 3 / 3 / 1 |
| 视频公开链接 | MIT要求放入rviz_drone_flight.txt | —，尚待提供 |

## 原理通俗讲解

交付文件告诉读者做了什么、为什么这样做、结果怎样。理论题里的阻力补偿只完成了推导，团队代码没有实施该补偿，报告不把它当作已验证的改进。

完整团队源码在code/controller_pkg，视频与bag在data/raw。PDF中提到的analysis目录在当前布局对应data/analysis；正式提交还需按老师要求分个人和团队仓库。

## 阅读导航

| **入口** | **用途** |
| --- | --- |
| [Lab3首页](../README.md) | 查看总任务与完成状态 |
| [完整操作手册](../review/操作与演示.md) | 按实际步骤准备、演示和录制 |
