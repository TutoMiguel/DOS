"""Patch the current Word canon without rebuilding its historical content."""
from pathlib import Path
from copy import deepcopy
import json
import re
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from consolidar_reparto_capilar import STAGE, WORK, PLAN, HEADING, POLICY, SUMMARY, read, counts

SOURCE=WORK/'Canon V16 Maestro.docx'
OUTPUT=STAGE/'word'/SOURCE.name

def shade(cell,fill):
    pr=cell._tc.get_or_add_tcPr()
    node=OxmlElement('w:shd');node.set(qn('w:fill'),fill);pr.append(node)

def add_table(doc,rows):
    table=doc.add_table(rows=1,cols=3)
    table.style='Table Grid'
    table.autofit=False
    widths=[Inches(2.15),Inches(1.85),Inches(1.85)]
    for col,width in zip(table.columns,widths):col.width=width
    for cell,text in zip(table.rows[0].cells,['Casa','Cabello del hombre','Cabello de la mujer']):cell.text=text
    header=OxmlElement('w:tblHeader');table.rows[0]._tr.get_or_add_trPr().append(header)
    for x in rows:
        for cell,text in zip(table.add_row().cells,['Casa '+x['name'],x['male'],x['female']]):cell.text=text
    borders=OxmlElement('w:tblBorders')
    for side in ['top','left','bottom','right','insideH','insideV']:
        node=OxmlElement('w:'+side)
        for key,value in [('val','single'),('sz','4'),('color','D9D9D9')]:node.set(qn('w:'+key),value)
        borders.append(node)
    table._tbl.tblPr.append(borders)
    for i,row in enumerate(table.rows):
        cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
        for cell in row.cells:
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                x=OxmlElement('w:'+side);x.set(qn('w:w'),'80');x.set(qn('w:type'),'dxa');margins.append(x)
            cell._tc.get_or_add_tcPr().append(margins)
            shade(cell,'E8EDF1' if i==0 else ('F6F8FA' if i%2==0 else 'FFFFFF'))
            for p in cell.paragraphs:
                p.paragraph_format.space_before=Pt(1);p.paragraph_format.space_after=Pt(2)
                p.paragraph_format.line_spacing=1.05
                p.paragraph_format.keep_with_next=(i==0)
                for r in p.runs:
                    r.font.name='Aptos';r.font.size=Pt(10);r.font.color.rgb=RGBColor(0,0,0)
                    r.bold=(i==0)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)

def main():
    plan=json.loads(read(PLAN));counts(plan)
    OUTPUT.parent.mkdir(exist_ok=True)
    doc=Document(SOURCE)
    original_count=len(doc.paragraphs)
    md=read(WORK/'Canon V16 Maestro.md')
    edits=[]
    for p in doc.paragraphs:
        for name in ('Fornost','Harnost','Mithlond'):
            if p.text.startswith('**'+name+':**') or p.text.startswith(name+':'):
                match=re.search(r'^- \*\*'+re.escape(name)+r':\*\* (.+)$',md,re.M)
                assert match,name
                p.clear();p.add_run(name+': ').bold=True;p.add_run(match.group(1));edits.append(name)
        if p.text.startswith('Las Casas Menores conservan su distribución geográfica y funcional.'):
            line=next(x for x in md.splitlines() if x.startswith('Las Casas Menores conservan su distribución geográfica y funcional.'))
            p.text=line;edits.append('resumen de Casas Menores')
    assert set(['Fornost','Harnost','Mithlond']).issubset(edits),edits
    doc.add_page_break()
    p=doc.add_heading(HEADING,level=1)
    for r in p.runs:r.font.color.rgb=RGBColor(0,0,0)
    doc.add_paragraph(POLICY)
    doc.add_paragraph(SUMMARY)
    doc.add_paragraph('Los perfiles familiares de Hallas, Thoron y Angren mantienen su referencia castaño claro y ojos verdes; '
                      'los de Fornost, Harnost y Mithlond mantienen sus tendencias pelirrojas y ojos celestes. '
                      'El color de cabello de cada representante sigue la asignación individual de las tablas. '
                      'Las quince Casas Mayores ya ilustradas y la Casa Real conservan su representación previa.')
    for cat,label in [('Casa Mayor','Casas Mayores pendientes de imagen'),('Casa Menor','Casas Menores'),('Casa Vasalla','Casas Vasallas')]:
        p=doc.add_heading(label,level=2)
        for r in p.runs:r.font.color.rgb=RGBColor(0,0,0)
        add_table(doc,[x for x in plan['allocation'] if x['category']==cat])
    doc.save(OUTPUT)
    verified=Document(OUTPUT)
    rows=[tuple(c.text for c in row.cells) for table in verified.tables[-3:] for row in table.rows[1:]]
    expected=[('Casa '+x['name'],x['male'],x['female']) for x in plan['allocation']]
    assert rows==expected and len(rows)==68
    assert len(verified.paragraphs)>original_count
    all_text='\n'.join(p.text for p in verified.paragraphs)
    for name in ('Fornost','Harnost','Mithlond'):
        assert re.search(re.escape(name)+r': Cabello pelirrojo; ojos celestes;',all_text),name
    report=dict(output=str(OUTPUT),local_profile_edits=edits,individual_rows=68,
                original_paragraphs=original_count,final_paragraphs=len(verified.paragraphs),
                original_tables=len(doc.tables)-3,final_tables=len(verified.tables))
    (STAGE/'verificacion_word.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
