"""Use the packaged DOCX renderer with a PDF exported by native Microsoft Word."""
from pathlib import Path
import importlib.util
import json
from pypdf import PdfReader

WORK=Path(__file__).resolve().parent
BASE=WORK/'consolidacion_capilar_casas'/'word'
DOCX=BASE/'Canon V16 Maestro.docx'
PDF=BASE/'Canon V16 Maestro.pdf'
RENDERER=Path(r'C:\Users\migue\.codex\plugins\cache\openai-primary-runtime\documents\26.1026.10807\skills\documents\render_docx.py')
spec=importlib.util.spec_from_file_location('document_renderer',RENDERER)
renderer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
assert PDF.is_file() and PDF.stat().st_size>10000
renderer.convert_to_pdf=lambda *args,**kwargs:(str(PDF),'PDF exported by native Microsoft Word')
dpi=renderer.calc_dpi_via_ooxml_docx(str(DOCX),1600,2000)
paths=renderer.rasterize(str(DOCX),str(BASE/'paginas'),dpi,verbose=False,emit_pdf=False)
reader=PdfReader(PDF)
assert len(paths)==len(reader.pages)
report=[]
for i,page in enumerate(reader.pages,1):
    text=page.extract_text() or ''
    report.append(dict(page=i,characters=len(text),gallery='Variación fenotípica y representantes' in text,
                       houses='Cabello del hombre' in text))
(BASE/'paginas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=len(paths),dpi=dpi,blank_pages=[x['page'] for x in report if x['characters']<20],
                     gallery_pages=[x['page'] for x in report if x['gallery'] or x['houses']]),ensure_ascii=False))
