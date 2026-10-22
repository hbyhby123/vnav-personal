"""Render the editable, review-friendly Markdown report without rewriting theory PDFs."""
from pathlib import Path
import html
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage

HERE = Path(__file__).resolve().parent
WIDTH = 499


def build_readable_report():
    regular = Path('C:/Windows/Fonts/msyh.ttc')
    bold = Path('C:/Windows/Fonts/msyhbd.ttc')
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
        'title': ParagraphStyle('readable_title', fontName=strong, fontSize=20, leading=28, spaceAfter=13),
        'h1': ParagraphStyle('readable_h1', fontName=strong, fontSize=14, leading=21,
                            spaceBefore=13, spaceAfter=7, keepWithNext=True),
        'h2': ParagraphStyle('readable_h2', fontName=strong, fontSize=11.4, leading=18,
                            spaceBefore=9, spaceAfter=6, keepWithNext=True),
        'body': ParagraphStyle('readable_body', fontName=normal, fontSize=10.2, leading=16,
                              spaceAfter=7, allowWidows=0, allowOrphans=0),
        'cell': ParagraphStyle('readable_cell', fontName=normal, fontSize=9, leading=14),
        'caption': ParagraphStyle('readable_caption', fontName=normal, fontSize=8.5, leading=13,
                                 alignment=1, spaceAfter=9),
    }

    def inline(text):
        text = html.escape(text).replace('−', '-').replace('ᵀ', '^T')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
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
            widths = [130, WIDTH-130]
        elif cols == 3:
            widths = [130, 145, WIDTH-275]
        elif cols == 4:
            widths = [90, 145, 135, WIDTH-370]
        else:
            widths = [WIDTH/cols]*cols
        cells = [[paragraph(c, 'cell') for c in row] for row in rows]
        tab = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT', rowSplitRange=(3, -2))
        tab.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dce8f0')),
            ('GRID', (0, 0), (-1, -1), .45, colors.HexColor('#d9d9d9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        return tab

    source = HERE/'实验报告.md'
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
        if line.startswith('|'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i].strip()); i += 1
            story.extend([table(block), Spacer(1, 9)])
            continue
        if line.startswith('# '):
            story.append(paragraph(line[2:], 'title'))
        elif line.startswith('## '):
            story.append(paragraph(line[3:], 'h1'))
        elif line.startswith('### '):
            story.append(paragraph(line[4:], 'h2'))
        elif line.startswith('!['):
            match = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if not match:
                raise ValueError(line)
            path = (HERE/match[2]).resolve()
            with PILImage.open(path) as im:
                width, height = im.size
            scale = min(WIDTH/width, 245/height)
            story.extend([Image(str(path), width=width*scale, height=height*scale, hAlign='CENTER'),
                          paragraph(match[1], 'caption')])
        elif line.startswith('- '):
            story.append(paragraph('• '+line[2:]))
        else:
            story.append(paragraph(line))
        i += 1

    def decoration(c, doc):
        c.setFont(normal, 8)
        c.drawString(48, 814, 'VNAV LAB4  无人机控制与竞速  |  黄博宇 24020036026')
        c.drawRightString(547, 27, str(doc.page))

    target = HERE/'Lab4_实验报告_黄博宇.pdf'
    doc = SimpleDocTemplate(str(target), pagesize=(595.276, 841.89), leftMargin=48, rightMargin=48,
                            topMargin=48, bottomMargin=43, title='Lab4 无人机控制与竞速实验报告', author='黄博宇')
    doc.build(story, onFirstPage=decoration, onLaterPages=decoration)
    print(target)


if __name__ == '__main__':
    build_readable_report()
