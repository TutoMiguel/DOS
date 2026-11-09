from pathlib import Path
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

root = Path(r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio')
src = root / 'Canon-Maestro-Unificado-Edicion-14.md'
out = root / 'Canon-Maestro-Unificado-Edicion-14.docx'
md = root / 'Canon-Maestro-Unificado-Edicion-14.md'

text = src.read_text(encoding='utf-8')
canonical = text.split('## Anexos documentales integrados')[0]

def clean(s):
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    s = s.replace('`','').replace('> ','')
    return s.strip()

# Create a cleaned Markdown companion.
cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', canonical).replace('`','')
md.write_text(cleaned, encoding='utf-8')

doc = Document()
sec = doc.sections[0]
sec.header.paragraphs[0].text = 'CANON MAESTRO VALINORIANO  |  EDICIÓN OPTIMIZADA 14'
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.text = '30 de octubre de 2026  •  Canon vigente'

title = doc.add_heading('Canon Maestro Optimizado de la Unión Valinoriana', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Edición 14 — 30 de octubre de 2026').alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Versión editorial optimizada: canon vigente, cronología, fichas consolidadas y registro de precedencia. Los documentos fuente permanecen como anexos externos trazables y no se mezclan visualmente con los datos operativos.')

doc.add_heading('Resumen canónico vigente', level=1)
for line in [
    'Valinor: 16 millones de habitantes.',
    'Valinor a Tyl: 26 millones.',
    'Aranath Valinor (Reino): 481 millones.',
    'Gwaith Valinor (Federación): 518 millones.',
    'Beleg Valinor (Gran Valinor): 710–860 millones.',
    'Gwaith Aear (Unión Marítima): 1.110–1.510 millones.',
    'PIB PPA de Gwaith Valinor: 60–69 billones; conciliación ECON-03 64,55 billones.',
    'Transición Círdan IV–Voronwë: 2030–2037.'
]: doc.add_paragraph(line, style='List Bullet')

doc.add_heading('Reglas de lectura', level=1)
doc.add_paragraph('Las cifras de las entidades superiores son acumulativas y no se suman entre niveles. Las decisiones más recientes del autor prevalecen sobre documentos anteriores. Los anexos históricos se conservan para trazabilidad, pero sus cifras sustituidas no son operativas.')

doc.add_heading('Índice de contenido consolidado', level=1)
for line in ['Jerarquía política y territorios','Cronología Maestra','Población y economía','Industrialización, motores, turbinas y microelectrónica','Armada y clases navales','Palantír-4D y Palantír Aeglos','Alianza con Chile y Gran Guerra del Pacífico','Magallanes y Andúnië Austral','Política cultural y acumulación del conocimiento','Registro de retcons y decisiones resueltas']:
    doc.add_paragraph(line, style='List Bullet')

doc.add_page_break()
for line in canonical.splitlines():
    line = line.rstrip()
    if not line: continue
    if line.startswith('# '): doc.add_heading(clean(line[2:]), level=1)
    elif line.startswith('## '): doc.add_heading(clean(line[3:]), level=1)
    elif line.startswith('### '): doc.add_heading(clean(line[4:]), level=2)
    elif line.startswith('#### '): doc.add_heading(clean(line[5:]), level=3)
    elif line.startswith('|'):
        # Render Markdown table rows as readable tab-separated text, without raw pipes.
        if set(line.replace('|','').replace('-','').replace(':','').strip()) == set():
            continue
        cells = [clean(x.strip()) for x in line.strip('|').split('|')]
        doc.add_paragraph('   •   '.join(cells))
    elif line.startswith('- '): doc.add_paragraph(clean(line[2:]), style='List Bullet')
    elif re.match(r'^\d+\. ', line): doc.add_paragraph(clean(line), style='List Number')
    else: doc.add_paragraph(clean(line))

doc.add_page_break()
doc.add_heading('Anexos documentales y trazabilidad', level=1)
doc.add_paragraph('Los siguientes archivos fueron integrados en el canon unificado. Se mantienen como fuentes históricas o temáticas; cuando discrepan, prevalece el resumen canónico vigente y el registro de retcons.')
for p in sorted(root.glob('*.md')):
    if p.name not in {src.name, md.name} and not p.name.startswith('Canon Maestro Optimizado'):
        doc.add_paragraph(p.name, style='List Bullet')
doc.add_paragraph('Esta edición evita reproducir la sintaxis Markdown de los anexos dentro del cuerpo principal. Las versiones completas permanecen en sus archivos originales.')
doc.save(out)
print(out)
print(md)
