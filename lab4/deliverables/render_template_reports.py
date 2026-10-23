"""Render bilingual Lab4 reports following the user-provided report template."""
from pathlib import Path
import html
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image, PageBreak, KeepTogether, CondPageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage

HERE = Path(__file__).resolve().parent
WIDTH = 499


def build_template_report(source_name='实验报告.md', target_name='Lab4_实验报告_黄博宇.pdf', english=False):
    regular = Path('C:/Windows/Fonts/times.ttf' if english else 'C:/Windows/Fonts/simsun.ttc')
    bold = Path('C:/Windows/Fonts/timesbd.ttf' if english else 'C:/Windows/Fonts/msyhbd.ttc')
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont('ReadableCJK', str(regular), subfontIndex=0))
        pdfmetrics.registerFont(TTFont('ReadableCJK-Bold', str(bold), subfontIndex=0))
        pdfmetrics.registerFontFamily('ReadableCJK', normal='ReadableCJK', bold='ReadableCJK-Bold',
                                     italic='ReadableCJK', boldItalic='ReadableCJK-Bold')
        normal, strong = 'ReadableCJK', 'ReadableCJK-Bold'
    else:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        pdfmetrics.registerFontFamily('STSong-Light', normal='STSong-Light', bold='STSong-Light',
                                     italic='STSong-Light', boldItalic='STSong-Light')
        normal = strong = 'STSong-Light'
    styles = {
        'title': ParagraphStyle('readable_title', fontName=strong, fontSize=22, leading=29, spaceAfter=18, alignment=1, textColor=colors.HexColor('#19354a')),
        'h1': ParagraphStyle('readable_h1', fontName=strong, fontSize=15, leading=21,
                            spaceBefore=16, spaceAfter=9, keepWithNext=True, textColor=colors.HexColor('#19354a')),
        'h2': ParagraphStyle('readable_h2', fontName=strong, fontSize=11.4, leading=18,
                            spaceBefore=11, spaceAfter=7, keepWithNext=True, textColor=colors.HexColor('#27475b')),
        'body': ParagraphStyle('readable_body', fontName=normal, fontSize=11, leading=14.8,
                              spaceAfter=7, allowWidows=0, allowOrphans=0),
        'cell': ParagraphStyle('readable_cell', fontName=normal, fontSize=9.5, leading=13),
        'caption': ParagraphStyle('readable_caption', fontName=normal, fontSize=8.5, leading=13,
                                 alignment=1, spaceAfter=9),
        'code': ParagraphStyle('annotated_code', fontName='Courier' if english else normal,
                               fontSize=8.2, leading=11.5, spaceAfter=0,
                               backColor=colors.HexColor('#f5f5f5'), leftIndent=6, rightIndent=6),
    }

    def inline(text):
        text = html.escape(text).replace('−', '-').replace('ᵀ', '^T')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: m.group(1) + ' (' + m.group(2) + ')', text)
        text = text.replace('²', '<super>2</super>').replace('³', '<super>3</super>')
        return text

    def paragraph(text, kind='body'):
        return Paragraph(inline(text), styles[kind])

    def table(block):
        rows = [[c.strip() for c in line.strip().strip('|').split('|')] for line in block]
        rows = [row for row in rows if not all(re.fullmatch(r'[:\- ]+', c) for c in row)]
        cols = len(rows[0])
        if cols == 2:
            widths = [225, WIDTH-225]
        elif cols == 3:
            widths = [110, 180, WIDTH-290]
        elif cols == 4:
            widths = [90, 145, 135, WIDTH-370]
        else:
            widths = [WIDTH/cols]*cols
        cells = [[paragraph('**'+c.replace('**','')+'**' if j == 0 else c, 'cell') for c in row] for j,row in enumerate(rows)]
        tab = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT', rowSplitRange=(3, -2))
        tab.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6eef3')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white,colors.HexColor('#f6f8fa')]),
            ('GRID', (0, 0), (-1, -1), .35, colors.HexColor('#cbd5df')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        return tab

    source = HERE/source_name
    lines = source.read_text(encoding='utf-8').splitlines()
    story, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        # Editorial notes are provided after the full Markdown report, not inside
        # the formal PDF; the PDF retains the final seven-point review list.
        if line == '## 修改说明':
            break
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            i += 1
            code_paragraphs = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                raw = lines[i].rstrip()
                escaped = html.escape(raw).replace(' ', '&#160;')
                if raw.lstrip().startswith('//'):
                    escaped = '<font color="#356956">'+escaped+'</font>'
                code_paragraphs.append(Paragraph(escaped or '&#160;', styles['code']))
                i += 1
            if len(code_paragraphs) <= 12:
                if story and isinstance(story[-1], Paragraph) and story[-1].style is styles['h2']:
                    heading = story.pop()
                    code_paragraphs.insert(0, heading)
                story.append(KeepTogether(code_paragraphs))
            else:
                story.extend(code_paragraphs)
            story.append(Spacer(1, 10))
            i += 1
            continue
        if line.startswith('|'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i].strip()); i += 1
            story.extend([table(block), Spacer(1, 9)])
            continue
        if line.startswith('# '):
            story.append(paragraph(line[2:], 'title'))
        elif line.startswith('## '):
            if line.startswith('## 附录') or line.startswith('## Appendix'):
                story.append(PageBreak())
            story.append(paragraph(line[3:], 'h1'))
        elif line.startswith('### '):
            if line.startswith('### A.3') or line == '### A.4 Part1.3':
                story.append(CondPageBreak(550 if line == '### A.3 Part1.2' else 650))
            story.append(paragraph(line[4:], 'h2'))
        elif line.startswith('!['):
            match = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if not match:
                raise ValueError(line)
            path = (HERE/match[2]).resolve()
            with PILImage.open(path) as im:
                width, height = im.size
            max_height = 520 if height > width else 300 if "05_" in path.name else 255
            scale = min(WIDTH/width, max_height/height)
            story.append(KeepTogether([Image(str(path), width=width*scale, height=height*scale, hAlign='CENTER'),
                          paragraph(match[1], 'caption')]))
        elif line.startswith('表') or re.match(r'Table [A-Z0-9]', line):
            story.append(Paragraph(inline(line), ParagraphStyle('table_caption', parent=styles['caption'], keepWithNext=True)))
        elif line.startswith('- '):
            story.append(paragraph('• '+line[2:]))
        elif line.startswith(('黄博宇 24020036026','Boyu Huang, 24020036026','实验记录：','Recorded experiment:')):
            story.append(paragraph(line, 'caption'))
        else:
            story.append(paragraph(line))
        i += 1

    def decoration(c, doc):
        c.setFont(normal, 8)
        c.setFillColor(colors.HexColor('#617585'))
        c.setStrokeColor(colors.HexColor('#cbd5df'))
        c.setLineWidth(.5)
        c.line(48, 805, 547, 805)
        c.drawString(48, 814, 'VNAV LAB4 | Boyu Huang 24020036026' if english else 'VNAV LAB4  无人机控制与竞速  |  黄博宇 24020036026')
        c.drawCentredString(297.6, 27, str(doc.page))

    target = HERE/target_name
    doc = SimpleDocTemplate(str(target), pagesize=(595.276, 841.89), leftMargin=48, rightMargin=48,
                            topMargin=48, bottomMargin=43, title='Lab4 UAV Control and Racing' if english else 'Lab4 无人机控制与竞速实验报告', author='Boyu Huang' if english else '黄博宇')
    doc.build(story, onFirstPage=decoration, onLaterPages=decoration)
    print(target)


if __name__ == '__main__':
    build_template_report()
    build_template_report('Lab4_Report_EN.md', 'Lab4_Report_EN_Boyu_Huang.pdf', english=True)
