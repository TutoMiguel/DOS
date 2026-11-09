from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

SOURCE = Path(r"C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\Canon V16 Maestro.md")
OUTPUTS = [
    Path(r"C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\Canon V16 Maestro.docx"),
    Path(r"C:\IA\ValinARI\Valinari\Valinari\10_Archivo\Documentos editoriales\Oficial\Canon V16 Maestro.docx"),
]

def add_table(doc, rows):
    if not rows:
        return
    cells = [c.strip().strip("|").strip() for c in rows[0].split("|")]
    table = doc.add_table(rows=1, cols=len(cells))
    table.style = "Table Grid"
    for i, value in enumerate(cells):
        table.rows[0].cells[i].text = value
    for line in rows[2:]:
        vals = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(vals) != len(cells):
            continue
        row = table.add_row()
        for i, value in enumerate(vals):
            row.cells[i].text = value

def build():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    doc = Document()
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10)
    title_done = False
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("---"):
            i += 1
            while i < len(lines) and not lines[i].startswith("---"):
                i += 1
            i += 1
            continue
        if line.startswith("# "):
            p = doc.add_paragraph(style="Title")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run(line[2:].strip())
            title_done = True
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
        elif line.startswith("#### "):
            doc.add_heading(line[5:].strip(), level=3)
        elif line.startswith("| ") and i + 1 < len(lines) and lines[i + 1].lstrip().startswith("|---"):
            rows = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            add_table(doc, rows)
            continue
        elif line.startswith("- "):
            doc.add_paragraph(line[2:].strip(), style="List Bullet")
        elif line[:2].isdigit() and line[2:3] == ".":
            doc.add_paragraph(line, style="List Number")
        else:
            doc.add_paragraph(line)
        i += 1
    for out in OUTPUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        doc.save(out)

if __name__ == "__main__":
    build()
