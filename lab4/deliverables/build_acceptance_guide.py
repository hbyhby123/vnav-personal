"""Build the three-page Chinese TA demonstration guide."""
from pathlib import Path
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak

HERE = Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('Guide', 'C:/Windows/Fonts/msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('GuideBold', 'C:/Windows/Fonts/msyhbd.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='GuideBold')
styles = {k: ParagraphStyle(k, fontName='GuideBold' if k in ('title','head') else 'Guide',
    fontSize=size, leading=leading, spaceAfter=8, wordWrap='CJK')
    for k,size,leading in [('title',21,29),('head',13,20),('body',10.5,17),('cell',9.5,15)]}
story=[]
def p(s,kind='body'):
    return Paragraph(escape(s),styles[kind])
def text(s,kind='body'):
    story.append(p(s,kind))
def table(headers, rows, widths):
    cells=[[p(s,'cell') for s in row] for row in [headers]+rows]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E3EDF5')),
        ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#CBD5DF')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),
        ('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.extend([t,Spacer(1,10)])

text('Lab4 助教验收讲解提纲','title')
text('黄博宇  |  24020036026  |  第8组  |  2026年10月22日')
text('第1页：先讲清楚做了什么','head')
text('开场可以直接这样说（约40秒）','head')
text('老师好，我的Lab4是在Lab3控制器基础上完成无人机竞速。可以把它理解为：Lab4负责规划路线，Lab3负责让无人机跟上路线。我先让无人机在第一道赛门附近稳定悬停，确认位置和控制正常；再把所有赛门连成平滑轨迹，让无人机依次飞过。本次已经完成一次完整通关，并保存了代码、截图、视频和bag，也就是ROS消息记录文件。')
text('四个Part各负责什么','head')
table(['部分','我做了什么','为什么要做'],[
 ['Part0 首门悬停','把第一道门设为固定目标，目标速度、加速度设为0。','先验证目标坐标和控制器，稳定后再跑全程。'],
 ['Part1.1 取得起点','读取无人机当前的位置和水平朝向，收到有效状态后再规划。','从真实起点出发，避免用未初始化的数据。'],
 ['Part1.2 生成轨迹','经过赛门位置，生成平滑的位置和朝向轨迹。','让转弯和速度变化更平顺；朝向跨过±180°时走短方向。'],
 ['Part1.3 发布目标','按经过的时间，每秒50次发送当前应到达的目标状态。','控制器不断比较目标和实际状态，再调整旋翼。']
],[100,203,196])
text('一句话记住','head')
text('先稳住，再规划，按时间发目标，控制器持续纠偏。闭环控制就是“看偏了多少，再往回修”。')

story.append(PageBreak())
text('第2页：按这个顺序演示','title')
text('重点：先展示悬停，再展示完整通关，最后用记录解释效果。')
table(['顺序','做什么','现场怎么说'],[
 ['1 环境与编译','展示环境和20个包全部编译成功截图。','环境是Ubuntu20.04.6和ROS Noetic，实验代码已经编译通过。'],
 ['2 首门悬停','启动模拟器、通信桥和首门悬停程序；展示稳定画面。','先把第一道门作为固定目标，确认无人机能稳定保持。'],
 ['3 切换竞速','停止悬停程序；重置模拟器；重新启动轨迹跟踪节点。','悬停和竞速不能同时发目标；重启节点可重新计算时间起点。'],
 ['4 完整通关','先开启录制，再启动航点发布程序；展示完整视频或现场飞行。','程序从当前起点规划，依次跟踪各个赛门的位置和朝向。'],
 ['5 数据与代码','展示bag信息、轨迹对比图及两个主要源码。','视频看通关过程，bag用于检查跟踪误差，源码说明实现方式。']
],[68,218,213])
text('只记住这些关键数字','head')
table(['项目','实际结果','怎么解释'],[
 ['控制参数','kx=2，kv=3，kr=3，komega=1','分别调节位置、速度、姿态和角速度反馈强度。'],
 ['时间倍率','time_scale=2.0','把估算的每段时间乘2，使飞行更从容。'],
 ['执行段位置误差','RMSE约5.64cm；最大约8.44cm','RMSE是把误差平方后平均再开方，反映整体跟踪水平。'],
 ['高度偏差','实际高度平均比目标低约5.47cm','这是执行段统计；具体原因尚未验证，不能直接归因。'],
 ['三种时长','规划轨迹134.17s；bag167.28s；视频160.75s','记录起止范围不同；规划时长不等于独立计时的竞速成绩。']
],[100,195,204])
text('结果怎么总结：本次完成一次完整通关，轨迹跟踪误差为厘米量级；尚未做多轮加速对比，不声称最快。')

story.append(PageBreak())
text('第3页：助教追问时这样答','title')
table(['常见问题','简短回答'],[
 ['为什么先悬停？','先检查坐标、目标消息和控制器。基础不稳，直接竞速很难定位问题。'],
 ['平滑轨迹怎么理解？','不是把门用折线硬连起来，而是让位置及其变化衔接得更顺。minimum snap是尽量减小位置四阶导数的平方积分，减少猛烈的变化。'],
 ['朝向为什么要展开？','例如179°到-179°，实际只差2°。展开角度后可避免误以为要转358°。'],
 ['8和4是不是实测速度、加速度？','不是。v_max=8、a_max=4在这份代码里用于估算每段时间，不能直接当成严格保证的飞行上限。'],
 ['误差怎么算？','用bag记录时间，把期望位置插值到实际状态的采样时刻，再计算两者距离。主要统计轨迹执行段，不把末尾长时间悬停混进去。'],
 ['为什么重置后还要重启节点？','只按模拟器R键不会让现有轨迹重新生成。重启轨迹节点，才能重新取得起点和开始时间。'],
 ['代码重点看哪里？','simple_traj_planner.cpp负责首门目标和赛门信息；trajectory_generation_node.cpp负责起点、轨迹生成和按时间发布。'],
 ['理论题和代码次数为何不同？','minimum snap理论在相应端点与连接条件下可用7次多项式；代码N=10表示10个系数，即9次。两者条件和实现设置不同。']
],[137,362])
text('理论题只抓两条主线','head')
text('D1：在满足端点条件的前提下，让运动代价尽量小。原约束下最优P(t)=t；增加终点速度为-2的约束后，最优解会改变，不能照搬原答案。')
text('D2：把长路线分段，再让相邻段接得顺。minimum snap对应r=4，理论每段7次、8个系数；不仅要数位置和连续条件，还要考虑优化带来的自然条件。完整推导见两份理论PDF。')
text('最后可以这样收尾','head')
text('这次我完成了从赛门信息、轨迹规划、目标发布到控制跟踪的完整流程，并用视频和消息记录保留证据。后续可以检查高度偏差，并在稳定通关的基础上逐步缩短时间。')
text('材料入口：GitHub / hbyhby123 / vnav-personal / lab4。报告在deliverables，原始视频和bag在data/raw，完整操作命令在review/操作与演示.md。')

def footer(c,doc):
    c.setFont('Guide',8)
    c.setFillColor(colors.HexColor('#64748B'))
    c.drawString(48,815,'VNAV LAB4  |  助教验收讲解提纲')
    c.drawRightString(547,26,f'{doc.page} / 3')

target=HERE/'Lab4_助教验收讲解提纲_黄博宇.pdf'
SimpleDocTemplate(str(target),pagesize=(595.276,841.89),leftMargin=48,rightMargin=48,
    topMargin=48,bottomMargin=43,title='Lab4 助教验收讲解提纲',author='黄博宇').build(
        story,onFirstPage=footer,onLaterPages=footer)
print(target)
