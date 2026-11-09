from pathlib import Path
from docx import Document

ROOT = Path(r"C:\Users\migue\OneDrive\DOS")
OUTPUTS = [
    ROOT / "Historia de un imperio ficticio" / "Canon V16 Maestro.docx",
    ROOT / "Valinari" / "10_Archivo" / "Documentos editoriales" / "Oficial" / "Canon V16 Maestro.docx",
]

TITLE = "Religión valinari y relaciones interconfesionales"
PARAGRAPHS = [
    "La religión valinari reconoce a Eru como principio creador y utiliza los relatos de Ainur y Maiar como categorías espirituales, literarias y culturales. No considera que existan especies sobrenaturales verificables.",
    "La expansión marítima convirtió a Valinor en una civilización plural. Las comunidades judías, católicas, musulmanas y budistas conservaron lugares de culto, escuelas, cementerios, festividades y autoridades religiosas. La ley federal prevalece en delitos, impuestos, defensa, ciudadanía y derechos civiles.",
    "El judaísmo influyó en la memoria histórica, los pactos, la interpretación textual, la medicina, las finanzas y el comercio. El catolicismo aportó instituciones hospitalarias, diplomacia, archivos, arquitectura y derecho comparado.",
    "El islam fue decisivo en astronomía, matemáticas, medicina, cartografía, navegación, óptica, ingeniería hidráulica y comercio, especialmente en Egipto, el mar Rojo, Adén, Socotra, Omán, el golfo y Malaca.",
    "El budismo influyó en educación monástica, medicina, disciplina intelectual, compasión, traducción y conservación de manuscritos en las rutas del Índico y Asia.",
    "Desde Forostar, la autoridad política, la autoridad sacerdotal y la investigación intelectual se distinguen institucionalmente. La Corona no puede declararse encarnación de Eru ni imponer una interpretación única. El principio canónico es el pluralismo pactado.",
]

for path in OUTPUTS:
    doc = Document(path)
    if not any(p.text.strip() == TITLE for p in doc.paragraphs):
        doc.add_heading(TITLE, level=1)
        for paragraph in PARAGRAPHS:
            doc.add_paragraph(paragraph)
        doc.save(path)
