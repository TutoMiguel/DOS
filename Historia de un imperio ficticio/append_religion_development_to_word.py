from pathlib import Path
from docx import Document

ROOT = Path(r"C:\Users\migue\OneDrive\DOS")
OUTPUTS = [
    ROOT / "Historia de un imperio ficticio" / "Canon V16 Maestro.docx",
    ROOT / "Valinari" / "10_Archivo" / "Documentos editoriales" / "Oficial" / "Canon V16 Maestro.docx",
]
TITLE = "Organización interna de la religión valinari"
TEXT = [
    "La religión valinari no es una iglesia única. Está formada por templos locales, Casas de la Memoria, santuarios de las estrellas, órdenes de guardianes, capellanías navales y escuelas teológicas.",
    "Los Templos de Eru celebran nacimientos, matrimonios y funerales, mantienen escuelas y prestan asistencia social. Las Casas de la Memoria conservan genealogías, tratados, mapas, registros de guerra y testimonios.",
    "El calendario combina ciclos solares, agrícolas y marítimos. Sus fiestas principales son el Día de la Primera Luz, la Fiesta de Forostar, la Noche de Elerwen, el Día de los Pactos, la Fiesta del Retorno y la Memoria de los Navegantes.",
    "La Corona se considera legítima mientras preserve pactos, santuarios, graneros, mercados, rutas y comunidades. Desde el siglo XVIII aumenta la secularización; en el siglo XIX los registros civiles, universidades, hospitales y tribunales adquieren autonomía respecto de los templos.",
    "En 1956 y 2026 Valinor mantiene una identidad religiosa propia, pero funciona como Estado pluralista con libertad de culto y separación entre religión, ciencia y administración.",
]
for path in OUTPUTS:
    doc = Document(path)
    if not any(p.text.strip() == TITLE for p in doc.paragraphs):
        doc.add_heading(TITLE, level=1)
        for paragraph in TEXT:
            doc.add_paragraph(paragraph)
        doc.save(path)
