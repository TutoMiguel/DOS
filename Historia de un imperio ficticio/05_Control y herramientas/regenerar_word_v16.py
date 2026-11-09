"""Regenerate the official Word from the active Markdown with native tables."""
from pathlib import Path
import re
import json
import hashlib
import statistics
import argparse
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\Users\migue\OneDrive\DOS\Valinari\00_Canon\Canon V16 Maestro.md')
WORK = ROOT / '.word_v16_regeneracion_20261105'
OUTPUT = WORK / 'Canon V16 Maestro.docx'


def plain(value):
    value = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m[1].split('|')[-1], value)
    value = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', value)
    value = value.replace('**', '').replace('`', '').replace('\\|', '|').replace('<br>', '\n').replace('<br/>', '\n')
    return re.sub(r'(?<!\w)\*([^*\n]+?)\*(?!\w)', r'\1', value)


def inline(paragraph, value, bold=False, italic=False):
    value = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m[1].split('|')[-1], value)
    value = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', value)
    value = value.replace('\\|', '|').replace('<br>', '\n').replace('<br/>', '\n')
    pattern = r'(\*\*.+?\*\*|(?<!\w)\*[^*\n]+?\*(?!\w)|`[^`]+`)' 
    for part in re.split(pattern, value):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            inline(paragraph, part[2:-2], True, italic)
        elif part.startswith('*') and part.endswith('*'):
            inline(paragraph, part[1:-1], bold, True)
        else:
            code = part.startswith('`') and part.endswith('`')
            run = paragraph.add_run(part[1:-1] if code else part)
            run.bold, run.italic = bold, italic
            if code:
                run.font.name = 'Consolas'
                run.font.size = Pt(9.5)


def cells(line):
    # Pipes inside Obsidian aliases are not table separators.
    line = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m[1].split('|')[-1], line)
    return [v.strip().replace('\\|', '|') for v in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def separator(line):
    return bool(line.strip().startswith('|') and all(re.fullmatch(r':?-{2,}:?', c.replace(' ', '')) for c in cells(line)))


def element(name, **attrs):
    e = OxmlElement('w:' + name)
    for k, v in attrs.items():
        e.set(qn('w:' + k), str(v))
    return e


def make_table(doc, lines, audit):
    records = [cells(x) for x in lines if not separator(x)]
    ncols = max(map(len, records))
    for row in records:
        row.extend([''] * (ncols - len(row)))
    wide = ncols > 10
    if wide:
        sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Inches(11), Inches(8.5)
    table = doc.add_table(rows=0, cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    available = 9.6 if wide else 7.1
    weights = []
    for col in range(ncols):
        lengths = sorted(len(plain(r[col])) for r in records)
        body = statistics.median(lengths) if lengths else 8
        weights.append(max(9, min(70, body)) ** 0.55)
    widths = [available * x / sum(weights) for x in weights]
    if ncols == 18:
        widths = [1.4, .58, .58, .65, .72, .62] + [.34] * 10 + [.82, .83]
    # Long headers must wrap rather than squeezing numeric values.
    minimum = .30 if wide else (0.58 if ncols >= 7 else 0.65)
    for _ in range(4):
        too_small = [i for i, w in enumerate(widths) if w < minimum]
        if not too_small:
            break
        shortfall = sum(minimum - widths[i] for i in too_small)
        large = [i for i in range(ncols) if i not in too_small]
        for i in too_small:
            widths[i] = minimum
        for i in large:
            widths[i] -= shortfall * widths[i] / sum(widths[j] for j in large)
    for col, width in zip(table.columns, widths):
        col.width = Inches(width)
    props = table._tbl.tblPr
    borders = element('tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        borders.append(element(edge, val='single', sz=4, color='D9D9D9'))
    props.append(borders)
    margins = element('tblCellMar')
    for edge, value in [('top', 85), ('bottom', 85), ('left', 90), ('right', 90)]:
        margins.append(element(edge, w=value, type='dxa'))
    props.append(margins)
    for rownum, record in enumerate(records):
        row = table.add_row()
        trpr = row._tr.get_or_add_trPr()
        if rownum == 0:
            trpr.append(element('tblHeader'))
        if max(map(len, record)) < 500:
            trpr.append(element('cantSplit'))
        for colnum, (cell, content) in enumerate(zip(row.cells, record)):
            cell.width = Inches(widths[colnum])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if rownum == 0:
                cell._tc.get_or_add_tcPr().append(element('shd', fill='E7E6E6'))
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.02
            p.paragraph_format.keep_with_next = False
            p.paragraph_format.widow_control = False
            if rownum and re.fullmatch(r'[\d.,%–—−\- /]+', plain(content)):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            inline(p, content, bold=rownum == 0)
            for run in p.runs:
                run.font.size = Pt(8.5 if wide else (9 if ncols >= 7 else 9.5))
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = Pt(3)
    audit.append({'columns': ncols, 'rows': len(records), 'header': records[0]})
    if wide:
        sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)


def build():
    WORK.mkdir(exist_ok=True)
    text = SOURCE.read_text(encoding='utf-8-sig')
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.7)
    sec.top_margin = sec.bottom_margin = Inches(0.7)
    styles = doc.styles
    for name in ['Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'List Bullet']:
        style = styles[name]
        style.font.name = 'Calibri'
        style.font.color.rgb = RGBColor(0, 0, 0)
        for border in style._element.xpath('.//w:pBdr'):
            border.getparent().remove(border)
    normal = styles['Normal']
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.widow_control = True
    for name, size, before, after in [('Title', 24, 0, 14), ('Heading 1', 16, 16, 8), ('Heading 2', 13, 12, 6), ('Heading 3', 11.5, 10, 5), ('Heading 4', 11, 8, 4)]:
        style = styles[name]
        style.font.size = Pt(size)
        style.font.bold = name != 'Title'
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    styles['List Bullet'].paragraph_format.space_after = Pt(3)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = element('fldSimple', instr='PAGE')
    footer._p.append(field)
    doc.core_properties.title = 'Canon V16 Maestro'
    doc.core_properties.subject = 'Canon vigente de la Unión Valinoriana'
    doc.core_properties.language = 'es-ES'
    doc.core_properties.comments = ''
    lines = text.splitlines()
    index, first_title, table_audit, consumed = 0, True, [], []
    while index < len(lines):
        line = lines[index].strip()
        if not line or re.fullmatch(r'[-*_]{3,}', line):
            index += 1
            continue
        if line.startswith('|') and index + 1 < len(lines) and separator(lines[index + 1]):
            block = []
            while index < len(lines) and lines[index].strip().startswith('|'):
                block.append(lines[index])
                index += 1
            make_table(doc, block, table_audit)
            consumed.extend(plain(c) for row in block if not separator(row) for c in cells(row))
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            count, content = len(heading[1]), heading[2]
            if first_title:
                p = doc.add_paragraph(style='Title')
                first_title = False
            else:
                p = doc.add_paragraph(style='Heading ' + str(min(4, max(1, count - 1))))
            inline(p, content)
            consumed.append(plain(content))
        elif re.match(r'^[-*+]\s+', line):
            content = re.sub(r'^[-*+]\s+', '', line)
            p = doc.add_paragraph(style='List Bullet')
            inline(p, content)
            consumed.append(plain(content))
        elif re.match(r'^\d+[.)]\s+', line):
            # Retain explicit ordinal numbers from the source.
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.22)
            p.paragraph_format.first_line_indent = Inches(-0.22)
            p.paragraph_format.space_after = Pt(3)
            inline(p, line)
            consumed.append(plain(line))
        else:
            quote = line.startswith('> ')
            content = line[2:] if quote else line
            p = doc.add_paragraph()
            if quote:
                p.paragraph_format.left_indent = Inches(0.2)
            inline(p, content, italic=quote)
            consumed.append(plain(content))
        index += 1
    doc.save(OUTPUT)
    reopened = Document(OUTPUT)
    all_text = '\n'.join(p.text for p in reopened.paragraphs) + '\n' + '\n'.join(c.text for t in reopened.tables for r in t.rows for c in r.cells)
    anomalies = [p.text[:100] for p in reopened.paragraphs if p.text.startswith('|') or '**' in p.text or '[[' in p.text]
    missing = [s[:100] for s in consumed if s and s not in all_text]
    assert len(reopened.tables) == len(table_audit)
    assert not anomalies, anomalies[:10]
    # Any differences from italic punctuation are reviewed separately.
    report = {'source': str(SOURCE), 'output': str(OUTPUT), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'paragraphs': len(reopened.paragraphs), 'tables': len(table_audit), 'table_rows': sum(t['rows'] for t in table_audit), 'unmatched_content': missing, 'table_inventory': table_audit}
    (WORK / 'verificacion.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'table_inventory'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--work', type=Path, default=WORK)
    args = parser.parse_args()
    SOURCE, WORK = args.source.resolve(), args.work.resolve()
    OUTPUT = WORK / 'Canon V16 Maestro.docx'
    build()
