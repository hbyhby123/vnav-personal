"""Build the report and two theory PDFs from measured JSON and uploaded evidence."""
from pathlib import Path
import json
import html
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from PIL import Image as PILImage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'deliverables'
ASSETS=OUT/'assets/equations'
ASSETS.mkdir(parents=True,exist_ok=True)
M=json.loads((BASE/'data/analysis/metrics.json').read_text())
SHOTS=BASE/'data/raw/screenshots'
font=Path('C:/Windows/Fonts/simhei.ttf')
if font.exists():
    pdfmetrics.registerFont(TTFont('CJK',str(font)))
else:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    # The CID alias permits Linux recreation with its available CJK fallback.
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    pdfmetrics.registerFontFamily('CJK',normal='STSong-Light')
    font=None
FONT='CJK' if font else 'STSong-Light'
S={
 'title':ParagraphStyle('title',fontName=FONT,fontSize=21,leading=28,spaceAfter=16,textColor=colors.black),
 'h1':ParagraphStyle('h1',fontName=FONT,fontSize=15,leading=22,spaceAfter=10,spaceBefore=2,textColor=colors.black),
 'h2':ParagraphStyle('h2',fontName=FONT,fontSize=11.5,leading=17,spaceAfter=7,spaceBefore=9),
 'body':ParagraphStyle('body',fontName=FONT,fontSize=10,leading=16,spaceAfter=8),
 'small':ParagraphStyle('small',fontName=FONT,fontSize=8.4,leading=13,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName=FONT,fontSize=8.8,leading=13),
 'caption':ParagraphStyle('caption',fontName=FONT,fontSize=8.5,leading=13,alignment=TA_CENTER,spaceAfter=10),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8.2,leading=12,spaceAfter=7)
}
WIDTH=499
def P(text,style='body'):
    for a,b in [('ᵀ','^T'),('²','^2'),('¹','^1'),('³','^3'),('−','-'),('‴',"'''"),('–','-'),('—','-')]:
        text=text.replace(a,b)
    return Paragraph(html.escape(text).replace('\n','<br/>'),S[style])
def T(headers,rows,widths=None):
    data=[[P(x,'cell') for x in headers]]+[[P(str(x),'cell') for x in row] for row in rows]
    t=Table(data,colWidths=widths or [WIDTH/len(headers)]*len(headers),repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbe8f1')),
      ('GRID',(0,0),(-1,-1),.45,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
      ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
      ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t
def img(path,maxw=WIDTH,maxh=235):
    with PILImage.open(path) as im:w,h=im.size
    scale=min(maxw/w,maxh/h)
    return Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')
def shot(number):return next(SHOTS.glob(number+'_*'))
eqcount=0
def EQ(tex):
    global eqcount
    eqcount+=1;p=ASSETS/f'eq_{eqcount:02d}.png'
    tex=re.sub(r'\\mathbf ([a-zA-Z])',r'\\mathbf{\1}',tex)
    tex=tex.replace(r'\frac14',r'\frac{1}{4}').replace(r'\frac92',r'\frac{9}{2}')
    fig=plt.figure(figsize=(8,.65));fig.text(.5,.45,'$'+tex+'$',ha='center',va='center',fontsize=15)
    fig.savefig(p,dpi=180,bbox_inches='tight',pad_inches=.08,transparent=False);plt.close(fig)
    return img(p,maxh=45)
def header(c,doc):
    c.setFont(FONT,8);c.setFillColor(colors.HexColor('#555555'))
    c.drawString(48,812,'VNAV LAB4  无人机控制与竞速  |  黄博宇 24020036026')
    c.drawRightString(547,28,f'{doc.page}');c.setFillColor(colors.black)
def build(name,story):
    d=SimpleDocTemplate(str(OUT/name),pagesize=(595.276,841.89),leftMargin=48,rightMargin=48,topMargin=48,bottomMargin=45,
      title=name.replace('.pdf',''),author='黄博宇',pageCompression=1)
    d.build(story,onFirstPage=header,onLaterPages=header)
def h(text):return P(text,'h1')
def sub(text):return P(text,'h2')
def cap(text):return P(text,'caption')
def br():return PageBreak()

# D1: all subquestions and exact finite-dimensional solutions.
d1=[P('Lab4 单段轨迹优化理论解答','title'),P('Deliverable 1  |  黄博宇 24020036026  |  2026年10月22日','small'),
 P('令P(0)=0，因此常数项p0=0。目标是在0到1内最小化速度平方积分，满足P(1)=1。QP即二次规划：代价是系数的二次式，约束是系数的线性方程。'),
 EQ(r'J=\int_0^1[P^{\prime}(t)]^2\,dt=\mathbf p^TQ\mathbf p,\qquad Q_{ij}=\frac{ij}{i+j-1}'),
 P('上式下标i、j从1开始。因为P′(t)=Σ i·pi·t^(i−1)，将平方展开并逐项积分就得到Q。系数始终按[p1,p2,...]排列。'),
 sub('第1问 一次多项式'),P('P(t)=p1·t，P(1)=1直接给出p1=1。因此最优P(t)=t，J=∫0¹1dt=1。'),
 sub('第2问 二次多项式'),
 T(['量','结果'],[['p','[p1, p2]ᵀ'],['Q','[[1, 1], [1, 4/3]]'],['A，b','A=[1,1]，b=1'],['代价展开','J=p1²+2p1p2+(4/3)p2²'],['最优解','p=[1,0]ᵀ，P(t)=t，J=1']],[90,409]),
 P('代入p1=1−p2可得J=1+p2²/3，故p2=0唯一最优。允许二次项并没有降低代价。'),
 sub('第3问 三次多项式'),
 T(['量','结果'],[['p','[p1, p2, p3]ᵀ'],['Q','[[1,1,1], [1,4/3,3/2], [1,3/2,9/5]]'],['A，b','A=[1,1,1]，b=1'],['最优解','p=[1,0,0]ᵀ，P(t)=t，J=1']],[90,409]),
 P('Euler–Lagrange方程给出P″(t)=0，所以最优轨迹为直线，与数值QP一致。由Cauchy–Schwarz不等式，J≥(∫0¹P′dt)²=1，等号要求P′为常数，因此增加二次、三次自由度也不能把代价降到1以下。'),
 br(),h('第4问 加入终点速度 P′(1)=−2'),
 P('这次端点仍为P(0)=0、P(1)=1，但终点速度被规定为−2。直线P=t已经不可行，必须重新求解有限次数的QP。'),
 EQ(r'\begin{bmatrix}2Q&A^T\\A&0\end{bmatrix}' ) if False else P('KKT线性方程：[[2Q, Aᵀ], [A, 0]] · [p; λ] = [0; b]。','code'),
 P('KKT是带约束最优点应满足的联立条件；第一块表示代价在可行方向上不能再下降，第二块就是原约束。Q正定，约束独立，因此各有限次数问题的解唯一。'),
 sub('第4(a)问 二次情形'),
 T(['量','结果'],[['Q','同第2问'],['A，b','A=[[1,1],[1,2]]；b=[1,−2]ᵀ'],['系数','p1=4，p2=−3'],['轨迹与导数','P=4t−3t²；P′=4−6t'],['约束检查','P(0)=0，P(1)=1，P′(1)=−2'],['最优代价','J=∫0¹(4−6t)²dt=4']],[90,409]),
 sub('第4(b)问 三次情形'),
 T(['量','结果'],[['Q','同第3问'],['A，b','A=[[1,1,1],[1,2,3]]；b=[1,−2]ᵀ'],['系数','p1=1/4，p2=9/2，p3=−15/4']],[90,409]),
 EQ(r'P(t)=\frac14t+\frac92t^2-\frac{15}{4}t^3,\qquad J^*=\frac{17}{8}=2.125'),
 P('也可以令p3=c，由两个约束消元得到p2=−3−2c、p1=4+c。代回代价可得J(c)=4+c+2c²/15，令导数1+4c/15=0得到c=−15/4。'),
 P('检查：P(1)=1/4+9/2−15/4=1；P′(1)=1/4+9−45/4=−2。三次情形把代价从4降到17/8，说明额外自由度在新约束下有用。'),
 P('复算：data/analysis/verify_theory.py使用有理数精确求解，并逐项验证端点、导数与积分。以上是题目有限次数模型的数学结论，不是飞行实测数据。','small'),
 P('来源：https://vnav.mit.edu/labs_2023/lab4/exercises.html；推导与核验于2026年10月22日完成。','small')]
build('deliverable_1.pdf',d1)

d2=[P('Lab4 多段轨迹优化理论解答','title'),P('Deliverable 2  |  黄博宇 24020036026  |  2026年10月22日','small'),
 P('以下按一维、各段时间固定、所有节点位置给定，起终点的1至r−1阶导数给定，内部节点的这些导数自由但相邻段连续来计数。三维位置可逐轴使用同样的推导；自由导数不等于导数为零。'),
 sub('第1问 最小 snap，r=4'),
 EQ(r'J=\sum_{j=1}^{k}\int_{t_{j-1}}^{t_j}[P_j^{(4)}(t)]^2\,dt'),
 P('snap是位置四阶导数。每段内部满足Euler–Lagrange方程Pj^(8)=0，所以一般解最高七次，每段8个系数，k段共有8k个未知数。相同位置在一个内部节点被左右两段各取一次，必须区分“节点数量”和“标量方程数量”。'),
 T(['条件类别','物理条件','标量方程数'],[
 ['航点位置','起点、终点各1式；内部k−1个位置左右各1式','2+2(k−1)=2k'],
 ['固定导数','起终点速度、加速度、jerk各给定；jerk是位置三阶导数','2×3=6'],
 ['自由导数的连续性','内部速度、加速度、jerk左右相等','3(k−1)'],
 ['自由导数的最优性','内部4、5、6阶导数左右相等','3(k−1)'],
 ['合计','2k+6+6(k−1)','8k']],[93,300,106]),
 P('按题目三类归并：waypoint共2k式；fixed derivative共6式；free derivative共6(k−1)式。内部自由导数变量只有3(k−1)个，但每种自由导数对应一条低阶连续条件和一条自然最优性条件，因此方程数是两倍。'),
 sub('为什么还要高阶连续条件'),
 P('对每段积分分部四次，边界项与δP、δP′、δP″、δP‴相乘。内部位置固定，δP=0；其余三种变化可自由但左右相同，因此对应的系数必须抵消，得到P^(4)、P^(5)、P^(6)连续。P^(7)不必连续，因为它乘的是已经为零的位置变化。'),
 P('这里的自然条件是最优性条件；在QP求解中通常由一阶最优条件自动产生，不能把它们全部说成用户额外施加的等式约束。'),
 br(),h('第2问 推广到 r 阶导数与 k 段'),
 EQ(r'J=\sum_{j=1}^{k}\int_{t_{j-1}}^{t_j}[P_j^{(r)}(t)]^2\,dt,\qquad P_j^{(2r)}=0'),
 P('因此每段最高2r−1次，有2r个系数，总未知数为2rk。在上述相同端点假设下，计数如下。'),
 T(['条件类别','一般数量','解释'],[
 ['waypoint','2k','k+1个物理位置；内部位置由左右段分别取值'],
 ['fixed derivative','2(r−1)','起终点各给定1至r−1阶导数'],
 ['free derivative','2(r−1)(k−1)','低阶连续与对应自然条件各(r−1)(k−1)式'],
 ['总计','2rk','2k+2(r−1)+2(r−1)(k−1)=2rk']],[110,140,249]),
 P('内部显式连续的是1至r−1阶导数；自然最优性条件要求r至2r−2阶导数连续。位置取值已固定，因此2r−1阶导数可以跳变。'),
 sub('显式QP约束与完整最优方程的区别'),
 T(['计数对象','一般r、k','r=4时'],[
 ['显式可行性约束','2k+2(r−1)+(r−1)(k−1)=(r+1)k+r−1','5k+3'],
 ['自然最优性条件','(r−1)(k−1)','3(k−1)'],
 ['完整方程','2rk','8k']],[135,258,106]),
 sub('用 k=3 检查最小 snap'),
 P('3段七次多项式有24个未知数。位置方程6个；起终点固定导数6个；两个内部节点的低阶连续6个；对应自然条件6个，合计24。显式QP约束18个，自然条件6个。'),
 sub('与本实验代码的关系'),
 P('理论给出最小snap变分解的最高七次；运行代码使用N=10，即每段10个系数、最高九次，并使用库提供的端点设置。不能把理论题的七次结论误写成代码N=7或声称代码恰好采用同一组边界约束。'),
 P('若端点导数不固定、部分内部导数也被固定，或把各段时间当作优化变量，上述计数需要相应修改。','small'),
 P('来源：https://vnav.mit.edu/labs_2023/lab4/exercises.html；计数恒等式由verify_theory.py对多组r、k核验。','small')]
build('deliverable_2.pdf',d2)

report=[P('Lab4 无人机控制与竞速实验报告','title'),P('黄博宇  24020036026  中外计科一班  第8组','body'),P('实验记录 run_20261022_000059  |  文档整理 2026年10月22日','small'),
 sub('实验概述'),
 P('本实验在TESSE Unity仿真赛道中，沿用Lab3几何控制器，补全首门悬停、当前位置读取、赛门轨迹优化和期望状态发布。用户已完成全部20个包编译、首门悬停及一次完整通关，并回传连续视频、原始bag、参数和完整源码。'),
 P(f'离线分析以参考轨迹执行段为主，位置RMSE为{M["execution"]["rmse_m"]:.4f} m，最大位置误差为{M["execution"]["max_m"]:.4f} m。参考轨迹总时长{M["planned_trajectory_duration_s"]:.2f} s，不能与bag总时长或独立裁判成绩混用。'),
 T(['任务','完成内容','对应材料'],[
 ['个人D1，20分','一至三次单段QP及新增终点速度约束','deliverable_1.pdf'],
 ['个人D2，15分','最小snap多段约束计数与r阶推广','deliverable_2.pdf'],
 ['团队D3，65分','四个Part、首门悬停、完整赛道运行','源码、截图、视频、bag'],
 ['可选加速','未做多轮速度优化比较','不申报最快队伍或额外成绩']],[99,270,130]),
 sub('环境与参数'),
 T(['项目','实际记录'],[
 ['系统与中间件','Ubuntu20.04.6 LTS；ROS Noetic；版本输出1.17.4'],
 ['工程与场景','VNAV2021；~/vnav_ws；~/vnav-builds/lab4'],
 ['控制增益','kx=2，kv=3，kr=3，komega=1'],
 ['轨迹设置','位置3维；yaw单维；N=10；时间倍率2.0；50Hz发布'],
 ['时间来源','use_sim_time=true；录制目录名保留原机器时间标签']],[116,383]),
 sub('通俗系统主线'),P('赛门CSV → ROS航点 → 平滑轨迹 → 按时间发送目标 → Lab3控制器 → 旋翼命令 → Unity状态反馈。ROS是连接程序的消息框架；闭环控制就是不断比较实际与目标，再纠正动作。'),
 br(),h('首门悬停与接口验证'),
 P('Part0读取第一道门的位姿，将位置与朝向填入期望状态，速度和加速度设为零，并广播world到desired_pose的坐标关系。位姿就是位置与朝向；TF用于表达坐标系之间的相对关系。'),
 T(['接口','格式','作用'],[
 ['/desired_traj_vertices','geometry_msgs/PoseArray','按顺序排列赛门位置和朝向'],
 ['/current_state','nav_msgs/Odometry','实际位置、方向与速度'],
 ['/desired_state','MultiDOFJointTrajectoryPoint','当前时刻的期望位置、速度等'],
 ['/rotor_speed_cmds','mav_msgs/Actuators','四个旋翼命令']],[132,183,184]),
 Spacer(1,12),img(shot('04'),maxh=220),cap('图1  用户首门悬停截图，保留原画面'),
 T(['方向','期望位置 m','实际位置 m','实际减期望 m'],[
 ['X','0.4226201','0.4226182','−0.0000019'],['Y','3.1652320','3.1652690','0.0000370'],['Z','2.6700000','2.6304210','−0.0395790']],[70,140,140,149]),
 P('该单次悬停读数显示水平误差很小、高度约低3.96厘米；它不是整段平均误差。飞行时使用的四个增益与2/3/3/1一致，随后切换完整竞速。'),
 br(),h('四个Part的实现与轨迹生成'),
 T(['位置','关键实现','作用'],[
 ['Part0','trajCB：首门目标与TF','先检查控制链是否接通'],
 ['Part1.1','onCurrentState：位置、yaw与有效状态标记','从真实当前位置开始规划'],
 ['Part1.2','位置3维、yaw单维；顶点约束；末端边界；角度展开','保持赛门顺序及朝向连续'],
 ['Part1.3','经过时间采样；填充消息数组；发布目标','让目标沿轨迹前进']],[76,276,147]),
 sub('朝向与时间'),
 P('yaw是水平方向的转向角。角度跨过±π时，先用相邻角差的等价短角展开，避免从179度突然绕一整圈去−179度。位置与yaw分别求解，但使用相同的段时间。'),
 EQ(r'\psi_i=\psi_{i-1}+\operatorname{atan2}(\sin(\psi_i^{raw}-\psi_{i-1}),\cos(\psi_i^{raw}-\psi_{i-1}))'),
 P('源码用速度8.0和加速度4.0估计各段时间，再乘time_scale=2.0。它们是时间估计参数，不是实际速度硬限幅。起点和终点用库的makeStartOrEnd设置边界；中间赛门只指定位置与yaw。'),
 EQ(r't_{sample}=\min(\max(t_{now}-t_{start},0),T)'),
 P('期望状态每秒发布50次。超过轨迹时长后继续发送末端目标，避免对越界时间求值。已有轨迹时节点不重新生成，因此新一轮必须停航点、停跟随器、复位，再按顺序重启。'),
 sub('控制器边界'),
 P('控制器读取位置、速度与方向，计算总力和力矩，再分配为旋翼转速。保留Lab3允许的简化：未加入期望角速度和角加速度前馈。归档保留用户原始代码；Lab3旧traj_tracking.launch默认增益仍是早期值，Lab4演示只用本实验两个launch，不启动旧圆轨迹发布器。'),
 br(),h('个人理论一 单段最小速度轨迹'),
 P('令P(t)=Σpi·t^i，P(0)=0。代价是速度平方积分，端点要求P(1)=1。QP是把多项式系数作为未知量的二次代价优化。'),
 EQ(r'Q_{ij}=\frac{ij}{i+j-1},\qquad \min_{\mathbf p}\mathbf p^TQ\mathbf p\quad\mathrm{s.t.}\quad A\mathbf p=b'),
 T(['次数','Q','A，b'],[
 ['1','[1]','[1]，1'],
 ['2','[[1,1],[1,4/3]]','[1,1]，1'],
 ['3','[[1,1,1],[1,4/3,3/2],[1,3/2,9/5]]','[1,1,1]，1']],[50,289,160]),
 P('三种情况下最优解都是P=t、J=1。Cauchy–Schwarz给出J≥1，Euler–Lagrange方程P″=0也给出直线，因此提高次数并不会自动降低原问题代价。'),
 sub('加入 P′(1)=−2 后'),
 T(['次数','约束矩阵A；b=[1,−2]ᵀ','最优轨迹','J'],[
 ['2','[[1,1],[1,2]]','4t−3t²','4'],
 ['3','[[1,1,1],[1,2,3]]','t/4+9t²/2−15t³/4','17/8']],[43,190,216,50]),
 P('二次解的系数由两个等式直接确定。三次情形可令p3=c，消去其余系数，得到J=4+c+2c²/15；极小值在c=−15/4处。增加自由度后代价从4降到2.125。'),
 P('这些数值是数学优化结果，不是飞行数据。完整矩阵、约束代回和积分见deliverable_1.pdf；精确有理数复算脚本为data/analysis/verify_theory.py。'),
 br(),h('个人理论二 多段轨迹的约束计数'),
 P('按一维、固定各段时间、节点位置已知、起终点1至r−1阶导数给定、内部低阶导数自由但连续计数。Euler–Lagrange给出每段P^(2r)=0，即最高2r−1次，总未知数2rk。'),
 T(['类别','r=4时','一般r阶'],[
 ['航点位置方程','2k','2k'],
 ['起终点固定导数','6','2(r−1)'],
 ['内部低阶连续','3(k−1)','(r−1)(k−1)'],
 ['内部自然最优条件','3(k−1)','(r−1)(k−1)'],
 ['完整方程数','8k','2rk']],[180,130,189]),
 P('k+1是物理位置数量；内部位置要被左右两段分别满足，故对应2k条标量方程。自由导数是允许优化器选择的导数值，不是默认设零。'),
 P('自然条件来自分部积分后的边界项：位置被固定，内部位置变化为零；其余低阶导数变化自由，于是r至2r−2阶导数需要连续。它们由最优性产生，不要全部当成额外施加给QP的用户约束。'),
 T(['计数口径','r=4，k=3示例'],[
 ['未知系数','3段×8=24'],['显式可行性约束','位置6+端点导数6+低阶连续6=18'],['自然最优条件','高阶连续6'],['合计','24，与未知数匹配']],[180,319]),
 P('题面free derivative类若按完整方程计数，应包含低阶连续及对应自然条件，共2(r−1)(k−1)式。代码N=10意味着最高九次，不应与本题七次变分解直接混为一谈。完整推导与不同端点假设说明见deliverable_2.pdf。'),
 br(),h('完整竞速结果与统计口径'),
 P('本次只有一轮回传的完整运行，用户确认全部赛门通过；视频显示连续飞行过程。航点消息含12个赛门位姿，代码在其前添加当前起点。下列统计只使用参考轨迹执行窗口，排除了完成后长时间保持。'),
 T(['指标','实测 / 分析结果','解释'],[
 ['记录总时长',f'{M["bag_duration_s"]:.2f} s','包含准备、飞行和末端保持'],
 ['参考轨迹时长',f'{M["planned_trajectory_duration_s"]:.2f} s','由time_from_start终值读取，不作裁判成绩'],
 ['执行段样本',str(M['execution']['samples']),'以实际状态时间为采样点'],
 ['三维位置RMSE',f'{M["execution"]["rmse_m"]:.4f} m','平方平均后开方，较大误差权重更大'],
 ['平均 / 最大误差',f'{M["execution"]["mean_m"]:.4f} / {M["execution"]["max_m"]:.4f} m','三维位置误差范数'],
 ['yaw RMSE',f'{M["execution_yaw_rmse_deg"]:.3f}°','先展开目标yaw，再按最短角差统计']],[120,125,254]),
 Spacer(1,8),img(BASE/'data/analysis/trajectory_xy.png',maxh=235),cap('图2  期望与实际水平轨迹；数字标注为赛门中心编号'),
 br(),h('跟踪误差与数据分析方法'),
 P('实际与目标消息使用同一bag记录时间。将期望位置、速度及展开后的yaw线性插值到实际状态时间，再计算实际减期望。执行起点由正在递增的目标消息中t记录−time_from_start的中位数估计，执行终点为该起点加参考轨迹总时长。'),
 img(BASE/'data/analysis/position_tracking.png',maxh=220),cap('图3  执行段XYZ目标与实际位置'),
 img(BASE/'data/analysis/tracking_error.png',maxh=210),cap('图4  三维误差与各轴误差'),
 P(f'各轴RMSE：X={M["execution_axis_rmse_m"][0]:.4f} m、Y={M["execution_axis_rmse_m"][1]:.4f} m、Z={M["execution_axis_rmse_m"][2]:.4f} m。Z轴平均实际减期望为{M["execution_axis_mean_error_m"][2]:.4f} m，高度偏低是本轮主要偏差。末端附近位置误差约{M["endpoint_error_m"]:.4f} m。','small'),
 br(),h('视频 截图与原始数据证据'),
 P('原视频时长160.75秒，包含准备和完整飞行。录屏为Ubuntu桌面，Unity窗口位于其中，画面中赛门颜色随穿越变化；截图06、07与连续视频相互补充。抽帧检查不能代替逐帧裁判，本报告采用用户完整通关确认并结合轨迹数据作一致性检查。'),
 img(shot('06'),maxh=190),cap('图5  竞速中途穿门截图'),
 img(shot('07'),maxh=190),cap('图6  运行末段截图，原始桌面与Unity画面均保留'),
 P('GitHub普通文件大小限制使原视频无法单文件上传，因此保存为3个分片，提供SHA256清单及自动还原脚本，确保可恢复逐字节一致的原视频。race_preview.mp4只做重新编码和缩放，不剪辑、不加速。原bag保持完整。'),
 br(),h('复现步骤 交付状态与结论'),
 T(['顺序','操作','检查'],[
 ['1','Unity启动Lab4，桥接连接ROS','实际状态有消息'],
 ['2','先static_point_test做首门悬停','确认稳定后Ctrl+C停止'],
 ['3','traj_following启动，time_scale=2.0','只有一套控制器'],
 ['4','record_race.sh开始录像和录bag','看到Video and bag recording'],
 ['5','traj_gen发布赛门','按顺序完整飞行'],
 ['6','通关后等3秒，录制终端Enter','bag正常收尾，检查视频和话题']],[40,300,159]),
 sub('故障与处理'),P('准备阶段先遇到gflags_catkin缺失和catkin_simple旧路径缓存，补源码依赖并备份重建；随后NLopt旧下载链路连接被拒绝，改为校验后的本地归档。用户最终回传All 20 packages succeeded，之后安装四个Part并再次全部编译成功。'),
 T(['交付项','状态'],[
 ['报告与两道理论题PDF','本次根据真实材料与推导生成'],
 ['完整源码、8张截图、原bag、视频','归档到code与data；原视频可还原'],
 ['分析CSV、图表、指标与复算脚本','归档到data/analysis'],
 ['Drive/Dropbox公开链接','用户尚未提供；GitHub备份不替代题面指定平台链接'],
 ['最快队伍 / 加速实验','未进行对比，不申报']],[190,309]),
 sub('实验结论'),P('已完成从赛门读取、轨迹优化、目标采样到控制器跟随的完整流程，并保留一次完整运行的可复核证据。轨迹执行段三维误差约为厘米级，主要偏差来自高度方向。后续可研究高度偏差和时间倍率，但本次没有伪造多轮提速结果。'),
 P('来源：MIT Lab4题面 https://vnav.mit.edu/labs_2023/lab4/exercises.html；VNAV2021代码 https://github.com/MIT-SPARK/VNAV-labs/tree/VNAV2021/lab4；所有实测指标来自用户回传run_20261022_000059。','small'),
 P('归档说明：理论推导、代码准备、离线分析与文档整理使用AI辅助；运行与截图来自用户Ubuntu。按所在课程要求保留相应辅助说明。','small')]
build('Lab4_实验报告_黄博宇.pdf',report)
print('Created 3 PDFs under',OUT)
