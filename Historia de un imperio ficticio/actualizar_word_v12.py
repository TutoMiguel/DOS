from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_BREAK
from pathlib import Path

src = Path(r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\Canon Maestro de la Union Valinoriana v12.docx')
out = Path(r'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\Canon Maestro de la Union Valinoriana v12 actualizado.docx')

doc = Document(src)
# Actualiza el encabezado editorial de la copia sin alterar el historial narrativo.
for p in doc.paragraphs[:3]:
    if 'Edición acumulativa 11' in p.text:
        for run in p.runs:
            run.text = run.text.replace('Edición acumulativa 11', 'Edición acumulativa 12')
            run.text = run.text.replace('29 de octubre de 2026', '30 de octubre de 2026')
        break
doc.add_page_break()
doc.add_heading('Actualización canónica consolidada — edición 12', level=1)
doc.add_paragraph('Fecha de consolidación: 30 de octubre de 2026. Esta sección actualiza la narración anterior con las decisiones acumulativas aprobadas en el proyecto. Cuando existe una formulación incompatible, prevalece esta sección; el texto histórico anterior se conserva como registro editorial y no como una segunda versión simultánea del canon.')

doc.add_heading('1. Jerarquía política vigente', level=2)
for text in [
    'Valinor a Tyl (Valinor + islas atlánticas): núcleo insular del sistema.',
    'Aranath Valinor (Reino de Valinor): núcleo insular más los territorios directos americanos y caribeños.',
    'Gwaith Valinor (Federación Valinoreana): Reino más Malaca, Hawái, Fiyi, Polinesia y Micronesia.',
    'Beleg Valinor (Gran Valinor): Federación más protectorados y enclaves de Oriente Medio, Mediterráneo, mar Rojo y África oriental.',
    'Gwaith Aear (Unión Marítima): Gran Valinor más aliados extranjeros; los aliados conservan soberanía y no se cuentan como provincias federales.'
]:
    doc.add_paragraph(text, style='List Bullet')

doc.add_heading('2. Territorios directos y equivalencias geográficas', level=2)
doc.add_paragraph('El canon usa equivalencias reales de referencia para ubicar unidades ficticias; no transforma automáticamente cada país moderno completo en una frontera jurídica ficticia. Las ciudades se escriben con el nombre del universo primero y el nombre real entre paréntesis.')
for text in [
    'Reino: Valinor; Tol Eressëa; Númenor (Terranova, como territorio asociado sin isla ficticia adicional); Arnor (Ontario, Quebec, Labrador, Nueva Escocia, Nuevo Brunswick, Isla del Príncipe Eduardo y Maine); Nosselië Toliva (Canarias); Sírënandë (Guyana, Surinam y Guayana Francesa); Venezuela Federal; Provincia del Orinoco; Calenardhon Austral (Río Grande do Sul y Santa Catarina); Colombia Costera; Panamá Federal; Trinidad; Tobago; Bahamas; Bermudas y Barbados.',
    'Federación: Reino más Malaca, Hawái, Fiyi, Polinesia, Micronesia y Systreyjar cuando se use como unidad insular federal independiente.',
    'Protectorados y enclaves de Gran Valinor: Eryndor (Baréin), Rhunost (Musandam), Harnen (Omán), Kheled-zâram (Kuwait), Círdan (Socotra), Harlond (Adén), Amon Rûdh (Yibuti), Alqualondë (Chipre), Eglarest (Malta) y Pelargir (Alejandría).',
    'Unión Marítima: Himring (Japón), Cuiviénen (Australia), Elenna (Nueva Zelanda), Doriath Oriental (Corea del Sur), Esgaroth del Pacífico (Singapur), Tirion Mediterránea (Italia), Eriador Occidental (España), Hithlum Meridional (Francia), Aldburg (Sudáfrica), Harad Occidental (Marruecos), Rhovanion Oriental (Turquía) y Pelargir Africana (Egipto), como aliados.'
]:
    doc.add_paragraph(text, style='List Bullet')

doc.add_heading('3. Secuencia atlántica consolidada', level=2)
for text in [
    '150 a. C. — primer contacto caribeño y establecimiento de rutas meridionales desde Madeira y Canarias.',
    '340–350 d. C. — descubrimiento de Tol Eressëa por la ruta norte.',
    '400–500 d. C. — llegada a Terranova; Númenor queda asociada a esa región, sin contorno insular ficticio separado.',
    '650–750 d. C. — descubrimiento de Valinor, al sur y al este de Tol Eressëa.',
    '750–850 d. C. — primeros asentamientos permanentes valinorianos en Valinor y consolidación de los corredores atlánticos.',
    '920–980 d. C. — asentamiento permanente de Númenor/Terranova dentro del sistema asociado.'
]:
    doc.add_paragraph(text, style='List Bullet')

doc.add_heading('4. Población y economía de referencia para 2026', level=2)
doc.add_paragraph('El total federal canónico vigente es de 245.050.000 residentes. El Núcleo Histórico Marítimo (100.000.000) está incluido en ese total y nunca se suma por segunda vez. La Unión Marítima es una categoría política ampliada: su población y PIB no deben presentarse como población federal valinoriana, porque incorpora aliados soberanos.')
doc.add_paragraph('Para el escenario económico consolidado, la Federación/Gran Valinor se mantiene como una economía de escala continental: PIB PPA aproximado de 60–72 billones de dólares internacionales y PIB nominal aproximado de 45–55 billones, sujetos a desglose posterior por unidad. Estas cifras son del canon alternativo y no son datos de la historia real.')

doc.add_heading('5. Auditoría de coherencia', level=2)
checks = [
    ('Cronología', 'Coherente tras separar el Caribe (150 a. C.), Tol Eressëa (340–350 d. C.), Terranova (400–500 d. C.) y Valinor (650–750 d. C.).'),
    ('Geografía', 'Coherente: Valinor queda al sur y al este de Tol Eressëa; Númenor se ubica en Terranova; Calenardhon Austral queda en el sur de Brasil; Nosselië Toliva corresponde a Canarias.'),
    ('Estatus político', 'Coherente: los aliados de la Unión Marítima no se convierten en provincias; los protectorados se distinguen de los territorios directos.'),
    ('Población', 'Coherente con una sola contabilidad: los subtotales del Núcleo Histórico Marítimo y del componente federal restante están incluidos en el total federal.'),
    ('Nomenclatura', 'Coherente con la regla primordial: nombres ficticios primero y nombre real entre paréntesis; no se reutilizan nombres para crear nuevas ciudades.'),
    ('Cartografía', 'Los mapas generados durante el intercambio no forman parte del canon. La ubicación oficial se expresa aquí mediante coordenadas y equivalencias textuales; no se adopta ningún contorno cartográfico no aprobado.'),
    ('Estado de lagunas', 'Siguen pendientes los polígonos jurídicos completos, el desglose demográfico por cohortes de todas las provincias y algunos padrones urbanos históricos. No se presentan como hechos cerrados.')
]
for label, result in checks:
    p = doc.add_paragraph()
    p.add_run(label + ': ').bold = True
    p.add_run(result)

doc.add_heading('6. Regla de precedencia', level=2)
doc.add_paragraph('Esta edición no borra la edición 11 ni sus antecedentes: los conserva como historial. Para futuras ampliaciones, la autoridad será: canon aprobado expresamente por el autor; esta actualización consolidada; cronología maestra y enmiendas acumulativas; documentos anteriores; inferencias y propuestas. Toda hipótesis nueva deberá quedar etiquetada como propuesta hasta su aprobación explícita.')

doc.save(out)
print(out)
