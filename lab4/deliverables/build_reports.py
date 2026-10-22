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

# The main report now renders directly from its editable Markdown source.
from render_readable_report import build_readable_report
build_readable_report()
print('Created 3 PDFs under', OUT)
