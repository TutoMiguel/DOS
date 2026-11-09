from pathlib import Path
import re, shutil
from docx import Document
from docx.shared import Pt

vault=Path(r'C:\Users\migue\OneDrive\DOS\Valinari')
prompt=vault/'09_Politica'/'Prompts Visuales de las 84 Casas.md'
text=prompt.read_text(encoding='utf-8')
sections=re.findall(r'^## (Casa .+?)\n(.*?)(?=^## Casa |\Z)',text,re.M|re.S)
rows=[]
for name,body in sections:
    m=re.search(r'\*\*Alturas consolidadas para la imagen:\*\* hombre ([^;]+); mujer ([^.]+)\.',body)
    if not m: raise RuntimeError(f'Altura faltante: {name}')
    rows.append((name,m.group(1).strip(),m.group(2).strip()))
targets=[
 Path(r'C:\Users\migue\OneDrive\DOS\Historia de un imperio ficticio\Canon V16 Maestro.docx'),
 Path(r'C:\Users\migue\OneDrive\DOS\Valinari\Canon V16 Maestro.docx'),
 Path(r'C:\Users\migue\OneDrive\DOS\Valinari\10_Archivo\Documentos editoriales\Oficial\Canon V16 Maestro.docx'),
]
stage=Path(r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\height-integration-20261102\docx')
stage.mkdir(parents=True,exist_ok=True)
for idx,src in enumerate(targets,1):
    if not src.exists(): continue
    doc=Document(src)
    # Remove an earlier generated section if present by deleting paragraphs/tables after marker.
    marker='Alturas consolidadas de representación visual de las 84 Casas'
    for p in list(doc.paragraphs):
        if p.text.strip()==marker:
            p._element.getparent().remove(p._element)
    doc.add_heading(marker, level=1)
    p=doc.add_paragraph('Estas alturas pertenecen a la dirección artística de los prompts de imagen y no constituyen datos biográficos obligatorios ni rasgos genéticos. Se miden de planta a coronilla, sin calzado ni adornos; los dos representantes deben aparecer sobre el mismo plano de suelo. La Casa Telcontar conserva su excepción aprobada de 1,97 m y 1,88 m.')
    table=doc.add_table(rows=1, cols=3)
    table.style='Table Grid'
    hdr=table.rows[0].cells
    hdr[0].text='Casa'; hdr[1].text='Hombre'; hdr[2].text='Mujer'
    for name,man,woman in rows:
        cells=table.add_row().cells
        cells[0].text=name; cells[1].text=man; cells[2].text=woman
    out=stage/f'{idx:02d}_{src.name}'
    doc.save(out)
print(f'ROWS={len(rows)} DOCX={len(list(stage.glob("*.docx")))}')
