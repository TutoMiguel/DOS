from pathlib import Path
from docx import Document
from docx.shared import Pt

root = Path(r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio')
master = root / 'actualizaciones_acumulativas_canon_v12.md'
out_md = root / 'Canon Maestro Unificado v13.md'
out_docx = root / 'Canon Maestro Unificado v13 actualizado.docx'

source_files = sorted(p for p in root.glob('*.md') if p.name not in {master.name, out_md.name} and not p.name.startswith('Canon Maestro Unificado'))

header = '''# Canon Maestro Unificado de la Unión Valinoriana — Edición 13\n\n**Estado:** CANON VIGENTE\n**Fecha de consolidación:** 30 de octubre de 2026\n\nEste archivo integra la actualización acumulativa vigente y conserva todos los documentos Markdown del proyecto como anexos trazables. La sección 17 de la actualización acumulativa contiene la escala demográfica vigente: Valinor 16 millones; Valinor a Tyl 26 millones; Aranath Valinor 481 millones; Gwaith Valinor 508 millones; Beleg Valinor 700–850 millones; Gwaith Aear 1.100–1.500 millones. La cifra federal anterior de 245.050.000 queda fuera del canon operativo.\n\n## Precedencia canónica\n\n1. Decisiones expresas más recientes del autor.\n2. Sección de retcon y escala vigente de `actualizaciones_acumulativas_canon_v12.md`.\n3. Cronología maestra y enmiendas v12 compatibles.\n4. Anexos históricos o documentos con cifras sustituidas, conservados para trazabilidad.\n\nLos anexos no reactivan cifras o reglas sustituidas cuando contradicen la sección vigente.\n\n## Índice de archivos integrados\n\n'''

parts = [header]
for p in source_files:
    parts.append(f'- `{p.name}`\n')
parts.append('\n## Canon acumulativo vigente\n\n')
parts.append(master.read_text(encoding='utf-8'))
parts.append('\n\n## Anexos documentales integrados\n\n')
for p in source_files:
    parts.append(f'\n# Anexo: {p.name}\n\n')
    parts.append(p.read_text(encoding='utf-8'))
    parts.append('\n')
out_md.write_text(''.join(parts), encoding='utf-8')

src_docx = root / 'Canon Maestro de la Union Valinoriana v12 actualizado.docx'
doc = Document(src_docx)
# Normaliza el encabezado editorial visible de la copia unificada.
for p in doc.paragraphs[:4]:
    for run in p.runs:
        run.text = run.text.replace('Edición acumulativa 11', 'Edición acumulativa 13')
        run.text = run.text.replace('EDICIÓN 11', 'EDICIÓN 13')
        run.text = run.text.replace('29 de octubre de 2026', '30 de octubre de 2026')
for section in doc.sections:
    for p in section.header.paragraphs:
        for run in p.runs:
            run.text = run.text.replace('EDICIÓN 11', 'EDICIÓN 13')
            run.text = run.text.replace('EDICIÓN 12', 'EDICIÓN 13')
    for p in section.footer.paragraphs:
        for run in p.runs:
            run.text = run.text.replace('29 de octubre de 2026', '30 de octubre de 2026')
# Corrige también la línea editorial dentro del cuerpo del documento.
for p in doc.paragraphs:
    for run in p.runs:
        run.text = run.text.replace('Edición acumulativa 12', 'Edición acumulativa 13')
        run.text = run.text.replace('Edición acumulativa 11', 'Edición acumulativa 13')
doc.add_page_break()
doc.add_heading('Canon Maestro Unificado — Edición 13', level=1)
doc.add_paragraph('Esta edición integra la actualización acumulativa vigente y el contenido de todos los archivos Markdown del proyecto. Los documentos fuente se conservan como anexos; cuando existe una contradicción, prevalece la resolución canónica más reciente del autor.')
doc.add_heading('Escala canónica vigente', level=2)
for line in [
    'Valinor: 16 millones de habitantes.',
    'Valinor a Tyl: 26 millones.',
    'Aranath Valinor: 481 millones.',
    'Gwaith Valinor: 508 millones.',
    'Beleg Valinor: 700–850 millones.',
    'Gwaith Aear: 1.100–1.500 millones.'
]:
    doc.add_paragraph(line, style='List Bullet')
doc.add_paragraph('La recalibración anterior de 245.050.000 habitantes queda fuera del canon operativo y se conserva solamente como antecedente editorial.')
doc.add_heading('Archivos Markdown integrados', level=2)
for p in source_files:
    doc.add_paragraph(p.name, style='List Bullet')
doc.add_heading('Anexos documentales', level=1)
for p in source_files:
    doc.add_page_break()
    doc.add_heading(f'Anexo: {p.name}', level=1)
    text = p.read_text(encoding='utf-8')
    for block in text.split('\n'):
        if block.startswith('# '):
            doc.add_heading(block[2:], level=2)
        elif block.startswith('## '):
            doc.add_heading(block[3:], level=3)
        elif block.strip():
            doc.add_paragraph(block)
doc.save(out_docx)
print(out_md)
print(out_docx)
