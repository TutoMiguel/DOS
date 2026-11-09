"""Generate individual visual art direction from the 84 current house notes."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(r'C:\IA\ValinARI\Valinari\Valinari\09_Politica')
WORK = Path(__file__).resolve().parent

# House | role for objects and clothing. These are image decisions, not biographies.
ROLE_DATA = '''Noldor|archivo
Vanyar|ceremonia
Teleri|astillero
Elwing|exploracion_hacha
Círdan|defensa_espada
Mithlond|exploracion_hacha
Esgal|lacustre
Calenhad|agricultura
Fornost|defensa_hacha
Annúminas|gobierno
Alqualondë|diplomacia
Armenelos|ciudades
Eldalondë|traduccion
Taur-en-Mor|bosques
Barad Calen|defensa_espada
Dol Amroth|defensa_espada
Pelargir|comercio
Harlond|derecho
Minas Anor|defensa_hacha
Eryn Lasgalen|bosques
Rhunost|defensa_hacha
Harnost|ambar
Eressëa Menel|astronomia
Calenor|caminos
Falastur|exploracion_espada
Círdanir|astillero
Ostor|reservas
Eärond|cartografia
Voronwë|exploracion_hacha
Meneldir|calendario
Thoron|mensajes
Elentir|faros
Lindor|archivo
Hallas|derecho
Gwindor|taller
Aglaran|defensa_hacha
Tarond|abastecimiento
Baranor|agricultura
Celepharn|traduccion
Maethor|defensa_espada
Belegor|exploracion_hacha
Duilin|medicina
Tumladen|agua
Angren|mineria
Erestor|pilotaje
Nimrodel|pesca
Falathar|exploracion_espada
Aerandir|navegacion
Calenard|agricultura
Rúmilion|calendario
Harlind|derecho
Erellont|exploracion_hacha
Aegnor|reservas
Amdir|ceremonia
Amrod|astillero
Anardil|mensajes
Ardamir|pilotaje
Araphor|cartografia
Barahir|defensa_espada
Belegund|agricultura
Brandir|defensa_hacha
Dírhael|gobierno
Ecthelion|diplomacia
Erchirion|comercio
Estelmo|traduccion
Findegil|archivo
Folcred|ganaderia
Forlong|defensa_espada
Galdor|credito
Hador|muelles
Hareth|mineria
Imrahil|bosques
Iorlas|defensa_hacha
Malbeth|ambar
Ohtar|astronomia
Oropher|lacustre
Saeros|salinas
Targon|asentamiento
Tuor|caravanas
Vorondil|metales
Wídfara|faros
Yavannor|astillero
Zirin|exploracion_espada
Telcontar|real'''
ROLES = dict(line.split('|') for line in ROLE_DATA.splitlines())

# Man's object | woman's object | background. All are portable or handheld.
OBJECT_DATA = '''archivo|un códice técnico o genealógico cerrado, apoyado en el antebrazo|un archivo portátil encuadernado y un estuche de plumas|una biblioteca con anaqueles de archivo
ceremonia|un libro de juramentos con cierre dorado|un medallón de oficio y un rollo de himnos|un salón ceremonial abierto al paisaje
astillero|una media maqueta portátil de casco naval|un plano de cuadernas y un compás de carpintero|una galería de astillero civil
exploracion_hacha|un hacha de embarque enfundada al cinturón|un diario de expedición y una carta de rutas|un mirador sobre rutas de exploración
exploracion_espada|una espada de viaje envainada al costado|un mapa de itinerarios y un registro de expedición|una galería sobre caminos y puerto
defensa_espada|una espada ceremonial envainada con tahalí heráldico|un hacha con el filo enfundado, sostenida verticalmente junto al muslo|un patio de capitanía y fortificaciones
defensa_hacha|un hacha de guardia con funda heráldica, sostenida junto al cuerpo|un plano de fortificaciones en un estuche rígido|un patio de fortaleza sobre el territorio
lacustre|una carta de vías interiores enrollada en su estuche|un registro de embarcaderos y un sello de paso|una logia sobre vías de agua navegables
agricultura|un libro de reservas y parcelas agrícolas|un pequeño haz ceremonial de espigas y una tablilla de inventario|una terraza sobre campos y graneros
gobierno|un registro administrativo encuadernado|un sello de oficina en cadena y un cuaderno de audiencias|una galería de gobierno y archivo
diplomacia|un tratado marítimo dentro de una carpeta de cuero|una carta diplomática sellada y un estuche de escritura|un pórtico de embajadas sobre las dársenas
ciudades|una maqueta portátil de puerta urbana|un libro de mercados y un manojo de espigas|una terraza sobre murallas, talleres y campos
traduccion|un códice bilingüe abierto sujeto con ambas manos|un pequeño glosario encuadernado y un pergamino sellado|una casa de traducción junto al puerto
bosques|un cuaderno forestal cerrado|un herbario de hojas prensadas y un recipiente cerrado de resina|una galería de madera sobre bosque y lago
comercio|un libro de aduanas y mercados|una pequeña balanza de pesas mercantiles en su estuche|una lonja sobre almacenes portuarios
derecho|un código de derecho marítimo abierto|un libro de contratos y un laudo sellado|una biblioteca jurídica y sala de arbitraje
ambar|un estuche de muestras de ámbar|un catálogo de intercambios y un sello mercantil|una logia de comercio báltico
astronomia|una pequeña esfera armilar de mano|un astrolabio portátil y un cuaderno de observación|una terraza de observatorio sobre el mar
caminos|un libro de caminos y peajes|una carta de itinerarios en portapergaminos|un pórtico sobre caminos y campos
reservas|un inventario encuadernado de existencias|un sello de almacén y una tablilla de provisiones|una logia de depósitos y graneros
cartografia|un atlas abierto sobre el antebrazo|un compás de dibujo y una carta astronómica enrollada|una cartoteca con cartas insulares y náuticas
calendario|un pequeño cuadrante astronómico de mano|un códice de calendarios y una tablilla de mareas|una terraza de observación con marcas solares
mensajes|un tubo sellado de despachos|un registro de relevos y una carta costera|una estación de mensajería sobre el litoral
faros|un farol portátil de señales finamente trabajado|un libro de señales y un cuadrante de mano|una galería de faro con observatorio
taller|un martillo de maestro artesano guardado en su estuche|una regla de trazado y un cuaderno de reparación|una galería junto a talleres de metalurgia
abastecimiento|un registro de provisiones navales|una carta de escalas y un sello de almacén|una galería de abastecimiento sobre naves
medicina|un herbario medicinal encuadernado|un estuche médico de cuero y un recipiente botánico cerrado|un jardín medicinal junto al puerto
agua|un plano de canales y un compás de trazado|un libro de fundación agrícola y una regla de medición|una terraza sobre acequias y campos
mineria|una muestra de mineral en un estuche y un pequeño martillo de ensayo|un cuaderno de vetas y una regla de taller|una galería sobre minas y hornos lejanos
pilotaje|una carta de bajos y canales en carpeta rígida|una cuerda de sondaje enrollada y un cuaderno de pilotaje|un mirador sobre estrechos rocosos
pesca|un libro de cabotaje y una muestra de cabo anudado|un registro pesquero y un sello de puerto|una galería sobre barcos de pesca y depósitos
navegacion|un cuaderno náutico y un tubo de mensajes|un cuadrante de mano y una carta de navegación de altura|una terraza sobre un puerto de expediciones
ganaderia|un libro de rebaños y provisiones|un cuaderno de abastecimiento y un broche pastoral|una galería sobre pastos y almacenes
credito|un libro de crédito mercantil|una póliza de navegación y un estuche de sellos|una sala de contratos sobre el puerto
muelles|una escuadra de carpintero y un cuaderno de reparación|un plano de muelles y una regla de trazado|una logia sobre muelles de reparación
salinas|un cuaderno de salinas y conservación|un pequeño recipiente cerrado de sal y un registro de provisiones|una galería sobre salinas y depósitos
asentamiento|una carta de islas y un acta de asentamiento|un libro de fundación y un sello de comunidad|una galería sobre una población insular
caravanas|un registro de caravanas y suministros|una carta de rutas terrestres y de cabotaje|una logia entre caminos y embarcaderos
metales|un estuche de muestras de metales|una balanza portátil y un libro de intercambios|una lonja de metales
real|un libro de juramentos con cierre de plata|un sello dinástico y un pergamino de pacto|una galería palaciega de Nueva Tirion'''
OBJECTS = {p[0]: p[1:] for p in (line.split('|') for line in OBJECT_DATA.splitlines())}

MALE_HAIR = [
    'corte corto a tijera, raya lateral y nuca despejada',
    'media melena hasta la mandíbula, apartada detrás de las orejas',
    'cabello hasta los hombros, suelto y peinado hacia atrás',
    'cabello largo hasta la parte alta de la espalda, en coleta baja',
    'corte medio a la nuca con dos trenzas finas en las sienes',
    'corte corto en laterales y coronilla más larga, sin degradado moderno',
    'cabello largo semirrecogido con broche heráldico discreto',
    'corte medio escalonado con raya central',
    'cabello hasta los hombros recogido en un moño bajo sencillo',
    'corte corto uniforme a tijera con flequillo lateral',
]
BEARDS = [
    'rostro completamente afeitado', 'barba corta de tres días',
    'barba corta de un centímetro con contornos cuidados',
    'barba media de tres centímetros y bigote integrado',
    'barba completa de cinco centímetros bien peinada', 'bigote discreto y mentón afeitado',
]
FEMALE_HAIR = [
    'cabello largo hasta media espalda, completamente suelto, raya central',
    'cabello hasta los hombros, corte recto y suelto detrás de las orejas',
    'cabello largo recogido en una trenza lateral ancha',
    'semirrecogido con dos trenzas de sien unidas por broche, resto suelto',
    'moño bajo trenzado, nuca despejada y dos mechones junto al rostro',
    'corona de trenzas con el resto del cabello recogido',
    'cabello largo en coleta baja atada con cinta heráldica',
    'corte escalonado a la clavícula, suelto y con raya lateral',
    'cabello largo parcialmente recogido en torsiones laterales',
    'recogido alto trenzado con horquillas discretas',
    'cabello a la mandíbula, corte corto a tijera y raya lateral',
    'cabello muy largo en una trenza central por la espalda',
]
MALE_POSES = [
    'de frente, hombros relajados y peso sobre la pierna derecha',
    'torso girado treinta grados hacia la mujer, barbilla horizontal y hombros abiertos',
    'de tres cuartos hacia fuera de la pareja, rostro vuelto hacia la cámara',
    'erguido, un pie ligeramente adelantado y rodillas relajadas',
    'de frente con el torso levemente inclinado hacia su compañera',
    'en tres cuartos, cabeza girada hacia la mujer y expresión serena',
    'en contrapposto suave, peso sobre la pierna izquierda',
]
FEMALE_POSES = [
    'de tres cuartos hacia el hombre, cabeza vuelta hacia la cámara',
    'de frente, un pie adelantado medio paso y hombros a distinta altura',
    'torso girado hacia fuera, mirada al hombre y mentón ligeramente elevado',
    'erguida, peso sobre la pierna izquierda y rostro hacia la cámara',
    'en contrapposto suave, hombros abiertos y barbilla horizontal',
    'torso orientado hacia el hombre y mirada hacia el horizonte',
    'de frente, cabeza levemente inclinada y postura relajada y solemne',
    'en tres cuartos, mirada hacia la cámara y pie derecho algo retrasado',
    'erguida, hombros equilibrados y cadera desplazada ligeramente a un lado',
    'un pie adelantado y el cuerpo orientado veinte grados hacia la cámara',
    'de tres cuartos hacia la cámara y mirada dirigida al objeto que porta',
]

def sections(text):
    matches = list(re.finditer(r'^##[ \t]+([^\n]+)$', text, re.M))
    return {m.group(1).strip(): text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
            for i, m in enumerate(matches)}

def clean(value):
    value = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', value)
    value = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m.group(1).split('/')[-1], value)
    return re.sub(r'\s+', ' ', value.replace('**', '')).strip()

def labelled(value, label):
    for line in value.splitlines():
        line = line.lstrip('- ').replace('**', '').strip()
        if line.casefold().startswith(label.casefold() + ':'):
            return line.split(':', 1)[1].strip()
    return ''

def matrix_rows():
    out = {}
    for line in (ROOT / 'Matriz Heráldica y Funcional de las Casas.md').read_text(encoding='utf-8-sig').splitlines():
        p = [c.strip() for c in line.strip('|').split('|')]
        if line.startswith('|') and len(p) in (5, 6) and p[1] in ROLES:
            out[p[1]] = dict(function=p[-3], charge=p[-2], palette=p[-1])
    return out

def houses():
    matrix = matrix_rows()
    out = []
    for folder, category, prefix in [('Casas Mayores','Casa Mayor','A'), ('Casas Menores','Casa Menor','M'),
                                     ('Casas Vasallas','Casa Vasalla','V'), ('Casa Real','Casa Real','R')]:
        indices = list((ROOT / folder).glob('Índice*.md'))
        order = {}
        if indices:
            order = {name:int(n) for n,name in re.findall(r'(?:^|\n)(?:[MV]-)?(\d+)\. \[\[Casa ([^\]]+)\]\]', indices[0].read_text(encoding='utf-8-sig'))}
        paths = sorted((ROOT / folder).glob('Casa *.md'), key=lambda p:(order.get(p.stem[5:],999),p.stem))
        for j,path in enumerate(paths,1):
            text = path.read_text(encoding='utf-8-sig')
            name = path.stem[5:]
            code = f'{prefix}-{order.get(name,j):02d}' if prefix != 'R' else 'R-25'
            out.append(dict(name=name, category=category, code=code, path=path, text=text, data=sections(text), matrix=matrix.get(name,{})))
    assert Counter(h['category'] for h in out) == {'Casa Mayor':24,'Casa Menor':24,'Casa Vasalla':35,'Casa Real':1}
    assert set(h['name'] for h in out) == set(ROLES)
    display_file=WORK/'orden_visual_casas.json'
    if display_file.exists():
        display=json.loads(display_file.read_text(encoding='utf-8'))
        assert len(display)==84 and set(display)==set(ROLES)
        out.sort(key=lambda h:display.index(h['name']))
    return out

def source_fields(h):
    d, m = h['data'], h['matrix']
    status = clean(d.get('Estatus',''))
    parent = re.search(r'^casa_tutelar:[ \t]*(.+)$',h['text'],re.M)
    parent = parent.group(1).strip() if parent else ''
    origin_block = d.get('Origen geográfico','')
    origin = labelled(origin_block,'Origen')
    if not origin and h['name'] == 'Telcontar':
        origin = 'Helsingborg; tradición familiar de exilio y retorno desde las tierras equivalentes a Finlandia.'
    function = labelled(origin_block,'Función histórica') or m.get('function','') or labelled(origin_block,'Característica histórica')
    visual = d.get('Carta heráldica y visual','')
    blazon = labelled(visual,'Blasón') or d.get('Blasón','')
    banner = labelled(visual,'Estandarte') or d.get('Estandarte','')
    if 'pendiente de ilustración' in blazon and m:
        blazon = f"Paleta {m['palette']}; motivo principal: {m['charge']}."
        banner = f"Estandarte vertical en {m['palette']}, con {m['charge']}."
    motto = labelled(visual,'Lema') or labelled(d.get('Lema',''),'Sindarin adaptado') or labelled(d.get('Lema',''),'Sindarin')
    inscription = labelled(visual,'Transcripción en alto tengwar') or labelled(d.get('Lema',''),'Transcripción en alto tengwar') or labelled(d.get('Lema',''),'Transcripción para alto tengwar')
    phenotype = d.get('Perfil fenotípico canónico','')
    if d.get('Perfil fenotípico cortesano'):
        phenotype += '\n\nPerfil cortesano específico:\n\n' + d['Perfil fenotípico cortesano']
    genotype = d.get('Genotipo poblacional orientativo','') or (
        'La ficha no fija un genotipo típico, alelos concretos ni frecuencias. Para estos representantes, '
        'la referencia poblacional es el perfil fenotípico canónico de la Casa y las asociaciones orientativas '
        'enumeradas a continuación. No se deducen estatura, complexión, personalidad ni peinado de estos genes.')
    genetics = d.get('Referencias genéticas orientativas','')
    assert all((origin,function,blazon,banner,motto,phenotype,genetics)), h['name']
    gallery = d.get('Representantes de la galería','')
    male_color = labelled(gallery,'Cabello del hombre')
    female_color = labelled(gallery,'Cabello de la mujer')
    assert bool(male_color) == bool(female_color), h['name']
    return dict(status=status, parent=parent, origin=clean(origin), function=clean(function), blazon=clean(blazon), banner=clean(banner),
                motto=clean(motto), inscription=clean(inscription), phenotype=phenotype, genotype=genotype, genetics=genetics,
                male_color=male_color, female_color=female_color)

def metres(cm):
    return f'{cm//100},{cm%100:02d} m'

def size(phenotype, i, female=False):
    t = phenotype.casefold()
    if any(x in t for x in ('robust','fuerte','musculatura desarrollada','musculatura marcada')):
        choices = ['complexión fuerte, hombros anchos y musculatura natural','complexión robusta y proporcionada, torso amplio']
    elif 'atlétic' in t:
        choices = ['complexión atlética y longilínea','complexión atlética, hombros medios y musculatura moderada']
    elif any(x in t for x in ('resistente','marinera','marítima')):
        choices = ['complexión firme, musculatura funcional moderada','complexión compacta y resistente, hombros medios']
    else:
        choices = ['complexión esbelta y proporcionada','complexión equilibrada, torso de anchura media','complexión longilínea y porte atlético suave']
    result = choices[(i+int(female))%len(choices)]
    return result + (', silueta legible bajo el vestido y proporciones naturales' if female else '')

def wardrobe(role):
    common = ('Túnicas largas y vestidos de corte de terciopelo, brocado y telas pesadas; bordados de oro y plata '
              'en cuello, mangas, cinturón y capa, subordinados a la paleta heráldica. Él lleva túnica ceñida, '
              'cinturón decorativo y capa; ella lleva vestido de escote alto, corpiño ajustado, mangas amplias '
              'y sobrevestido ornamentado. Joyas, broches, collares y emblemas de rango. Ropa y armaduras '
              'inspiradas en la estética cinematográfica de Tolkien. ')
    if role.startswith('defensa'):
        return common + 'Armadura ceremonial de láminas y malla sobre túnica larga, ambos rostros descubiertos y capas con forro de piel.'
    if role.startswith('exploracion'):
        return common + 'Capas de viaje ceremoniales con forro de piel, cuero trabajado y protección ligera selectiva.'
    if role in ('archivo','astronomia','calendario','traduccion','derecho','cartografia','medicina'):
        return common + 'Togas de estudio y bordados refinados; mangas ordenadas para exhibir libros e instrumentos con elegancia erudita.'
    if role == 'real':
        return common + 'Mantos dinásticos en plata, azul celeste y oro pálido, diademas discretas y joyas del pacto real.'
    return common + 'Vestuario cortesano adaptado al oficio mediante broches, cierres y bordados específicos.'

def make_record(h,i):
    f = source_fields(h)
    role = ROLES[h['name']]
    male_item,female_item,setting = OBJECTS[role]
    if h['name'] == 'Noldor':
        male_item = 'un códice técnico de metalurgia cerrado, apoyado en el antebrazo'
    elif h['name'] == 'Lindor':
        male_item = 'un códice genealógico cerrado, apoyado en el antebrazo'
    elif h['name'] == 'Findegil':
        male_item = 'un códice de derroteros cerrado, apoyado en el antebrazo'
    male_cm, female_cm = 177+(i*7)%26, 173+(i*5)%12
    if male_cm == female_cm:
        female_cm = 173+(female_cm-173+1)%12
    left = i%2 == 0
    ms,fs = ('izquierda','derecha') if left else ('derecha','izquierda')
    mx,fx = (28+i%4,68+i%3) if left else (69+i%4,28+i%3)
    mh = MALE_HAIR[i%len(MALE_HAIR)]
    beard = BEARDS[i%len(BEARDS)]
    fh = FEMALE_HAIR[(i*5+i//12)%len(FEMALE_HAIR)]
    if f['male_color']:
        mh = f'color {f["male_color"]}; ' + mh
        fh = f'color {f["female_color"]}; ' + fh
        if 'afeitado' not in beard or 'bigote' in beard:
            beard += f'; vello facial de tono {f["male_color"]}'
    mp,fp = MALE_POSES[i%len(MALE_POSES)],FEMALE_POSES[i%len(FEMALE_POSES)]
    mb,fb = size(f['phenotype'],i),size(f['phenotype'],i,True)
    relative = f'Él supera la altura de ella en {male_cm-female_cm} cm.' if male_cm>female_cm else f'Ella supera la altura de él en {female_cm-male_cm} cm; conservar esa diferencia en la imagen.'
    armed = role.startswith(('defensa','exploracion'))
    arms = ('Mostrar exclusivamente las armas asignadas: espadas envainadas y hachas con el filo cubierto por funda, porte ceremonial.'
            if armed else 'Ambos personajes van desarmados; sus objetos de oficio ocupan el lugar de las armas.')
    appearance = (
        f'Hombre adulto: altura corporal exacta {metres(male_cm)}, {mb}; {mh}; {beard}. '
        f'A la {ms} del espectador, centro corporal al {mx} % del ancho, {mp}; porta {male_item}. '
        f'Mujer adulta: altura corporal exacta {metres(female_cm)}, {fb}; {fh}. '
        f'A la {fs} del espectador, centro corporal al {fx} % del ancho, {fp}; porta {female_item}. {relative} '
        'Las alturas se miden de planta a coronilla, excluyendo calzado y adornos. Ambos de pie sobre el mismo '
        'pavimento horizontal, a igual profundidad y con suelas de igual grosor; pies y coronillas dentro del encuadre. '
        'No igualar líneas de ojos ni compensar alturas con escalones o perspectiva. '
        'Libros e instrumentos de mano delante del torso entre cintura y esternón; '
        'las armas conservan la posición indicada junto al muslo o cinturón; las manos libres relajadas. '
        + arms)
    banner = (
        f'Estandarte monumental visible detrás de ambos: {f["banner"]} Blasón: {f["blazon"]} '
        f'Nombre «Casa {h["name"]}» en la cabecera. En una banda bordada DENTRO del estandarte, incorporar '
        f'la transcripción en alto tengwar del lema «{f["motto"]}». La inscripción pertenece a la tela y sigue '
        'sus pliegues; situarla por encima de las cabezas y conservar su legibilidad. Emplear la grafía aprobada '
        'del lema; si sigue pendiente en la ficha, requiere composición o revisión específica. '
        'Tengwar es la escritura; conservar la lengua del lema según la ficha sin inventar otro lema.')
    priority_appearance = (
        'Para esta representación de Telcontar, priorizar el perfil cortesano: cabello plateado o rubio platino, '
        'ojos celestes y piel muy clara en ambos representantes. '
        if h['name'] == 'Telcontar' else '')
    if f['male_color']:
        priority_appearance += (
            f'Asignación individual de esta pareja: hombre de cabello {f["male_color"]}; '
            f'mujer de cabello {f["female_color"]}. Estas asignaciones de la galería tienen prioridad '
            'sobre el color de cabello descrito como tendencia familiar. Las parejas pueden tener '
            'distinto color natural de cabello por variación individual y matrimonios entre linajes. ')
        preserve_appearance = (
            'Conservar el color de ojos, piel, pecas y textura natural del cabello según la ficha; '
            'aplicar a cada representante su color capilar individual expresamente asignado. '
            'Los cortes y recogidos varían el peinado sin cambiar la textura ni los colores asignados. ')
    else:
        preserve_appearance = (
            'Conservar color de ojos, piel, pecas, color y textura natural del cabello según ese perfil. '
            'Los cortes y recogidos varían el peinado; no imponer ondas a un perfil de cabello liso ni cambiar su pigmentación. ')
    political_reference = f'Estatus: {f["status"]} '
    if f['parent']:
        political_reference += f'Casa tutelar de referencia histórica: {f["parent"]}; representar la heráldica propia de esta Casa Vasalla. '
    prompt = (
        f'Una imagen vertical 2:3 dedicada exclusivamente a Casa {h["name"]}, {h["category"].lower()}, '
        'con dos representantes adultos humanos anónimos, hombre y mujer de cuerpo entero. Galería heráldica '
        'de acabado pictórico realista y cinematográfico: arcos y columnas de piedra, luz natural dramática, '
        'textiles detallados y continuidad con la imagen de referencia. '
        + political_reference + f'Función histórica: {f["function"].rstrip(".")}. Origen: {f["origin"]} Fondo: {setting}. '
        + appearance + ' ' + wardrobe(role) + ' ' + banner + ' '
        f'Rasgos de ambos según el perfil de la Casa: {clean(f["phenotype"])} ' + priority_appearance +
        preserve_appearance +
        f'Genotipo poblacional orientativo correspondiente a esta Casa: {clean(f["genotype"])} '
        f'Referencias genéticas orientativas conservadas de su ficha: {clean(f["genetics"])} '
        'Rostros individualizados, facciones naturales, anatomía proporcionada y gestos sobrios. '
        'Sin retratos clonados, protagonistas adicionales, armas añadidas, armas de fuego, objetos contemporáneos, '
        'monitores, telescopios modernos ni orejas élficas.')
    source = h['path'].relative_to(ROOT).as_posix()[:-3]
    text = (
        f'## Casa {h["name"]}\n\n**Serie:** {h["code"]} · **Categoría:** {h["category"]} · '
        f'**Fuente:** [[{source}|Casa {h["name"]}]]\n\n'
        f'**Estatus:** {f["status"]}\n\n'
        + (f'**Casa tutelar:** {f["parent"]}\n\n' if f['parent'] else '') +
        f'**Función:** {f["function"]}\n\n**Origen:** {f["origin"]}\n\n'
        f'**Blasón vigente para esta representación:** {f["blazon"]}\n\n**Estandarte:** {f["banner"]}\n\n'
        f'**Lema:** {f["motto"]}\n\n**Estado de la grafía en alto tengwar en la fuente:** {f["inscription"]}\n\n'
        '### Distribución expresa de personajes\n\n'
        '| Personaje | Altura corporal | Tamaño y complexión | Cabello y barba | Posición y postura | Arma u objeto funcional |\n'
        '|---|---|---|---|---|---|\n'
        f'| Hombre | {metres(male_cm)} | {mb} | {mh}; {beard} | {ms.capitalize()}, al {mx} % del ancho; {mp} | {male_item} |\n'
        f'| Mujer | {metres(female_cm)} | {fb} | {fh} | {fs.capitalize()}, al {fx} % del ancho; {fp} | {female_item} |\n\n'
        f'{relative} Ambos de pie en el mismo plano de suelo y profundidad. {arms}\n\n'
        f'### Perfil fenotípico canónico\n\n{f["phenotype"]}\n\n'
        f'### Genotipo poblacional orientativo\n\n{f["genotype"]}\n\n'
        f'### Referencias genéticas orientativas\n\n{f["genetics"]}\n\n'
        f'### Prompt individual listo para copiar\n\n{prompt}\n')
    record = dict(name=h['name'], category=h['category'], code=h['code'], male_cm=male_cm, female_cm=female_cm,
                  male_side=ms, female_side=fs, male_pose=mp, female_pose=fp, male_hair=mh, beard=beard,
                  female_hair=fh, role=role, male_item=male_item, female_item=female_item, armed=armed,
                  source=str(h['path']), source_sha256=hashlib.sha256(h['text'].encode()).hexdigest(),
                  original_genotype=bool(h['data'].get('Genotipo poblacional orientativo')))
    record['visual_index']=i
    if f['male_color']:
        record['male_hair_color']=f['male_color']
        record['female_hair_color']=f['female_color']
    return text,record

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=WORK/'prompts_visuales_actualizados.md')
    parser.add_argument('--report',type=Path,default=WORK/'prompts_visuales_verificacion.json')
    args = parser.parse_args()
    catalog = houses()
    assignments_file=WORK/'asignaciones_visuales_casas.json'
    if assignments_file.exists():
        previous=json.loads(assignments_file.read_text(encoding='utf-8'))
        indices={r['name']:r.get('visual_index',i) for i,r in enumerate(previous)}
    else:
        indices={h['name']:i for i,h in enumerate(catalog)}
    chunks,records = [],[]
    for i,h in enumerate(catalog):
        text,record = make_record(h,indices[h['name']])
        chunks.append(text)
        records.append(record)
    lines = ['---','tipo: catálogo de prompts visuales','canon: V16','casas: 84','una_imagen_por_casa: true','---',
             '# Prompts Visuales de las 84 Casas','',
             'Una imagen por Casa. Cada prompt fija dos representantes adultos anónimos, alturas exactas, '
             'complexiones, peinados, posturas, posiciones y objetos de oficio. Son decisiones de representación '
             'para la galería, no nuevos datos biográficos ni eventos cronológicos.','',
             'Se conserva la estética cortesana valinoriana de referencia: terciopelos, brocados, bordados, '
             'arcos de piedra y vestuario de inspiración Tolkien. El lema aparece bordado dentro del estandarte '
             'en alto tengwar; las grafías todavía pendientes se indican conforme a las fuentes.','',
             'Los perfiles fenotípicos, los genotipos orientativos existentes y las referencias genéticas '
             'se conservan por Casa. Cuando una ficha carece de genotipo definido, se indica expresamente. '
             'Las alturas y peinados se asignan como dirección artística.','',
             '## Índice de distribución visual','',
             '| Serie | Casa | Categoría | Hombre | Mujer | Distribución | Objetos según función |',
             '|---|---|---|---|---|---|---|']
    for r in records:
        role_label = r['role'].replace('_',' ').replace('exploracion','exploración').replace('astronomia','astronomía').replace('cartografia','cartografía').replace('traduccion','traducción').replace('mineria','minería').replace('ganaderia','ganadería').replace('ambar','ámbar')
        lines.append(f'| {r["code"]} | [[#Casa {r["name"]}|Casa {r["name"]}]] | {r["category"]} | {metres(r["male_cm"])} | {metres(r["female_cm"])} | Hombre a la {r["male_side"]} | {role_label} |')
    grouped=[]
    current_category=None
    for chunk,record in zip(chunks,records):
        if record['category']!=current_category:
            current_category=record['category']
            grouped.append('# '+current_category)
        grouped.append(chunk)
    document = '\n'.join(lines)+'\n\n'+'\n\n'.join(grouped)+'\n'
    assert len(re.findall(r'^## Casa ',document,re.M)) == 84
    for heading in ('Perfil fenotípico canónico','Genotipo poblacional orientativo','Referencias genéticas orientativas','Prompt individual listo para copiar'):
        assert document.count('### '+heading+'\n') == 84,heading
    for i,r in enumerate(records):
        assert 177 <= r['male_cm'] <= 202 and 173 <= r['female_cm'] <= 184 and r['male_cm'] != r['female_cm']
        assert all(r[k] for k in ('male_item','female_item','male_pose','female_pose','male_hair','female_hair','beard'))
        for key in ('Perfil fenotípico canónico','Genotipo poblacional orientativo','Referencias genéticas orientativas','Perfil fenotípico cortesano'):
            original = catalog[i]['data'].get(key)
            if original:
                assert original in chunks[i],(r['name'],key)
    assert len(set((r['male_cm'],r['female_cm'],r['male_pose'],r['female_pose']) for r in records)) == 84
    assert {r['male_cm'] for r in records} == set(range(177,203))
    assert {r['female_cm'] for r in records} == set(range(173,185))
    args.output.write_text(document,encoding='utf-8')
    args.report.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    assignments_file.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(output=str(args.output),houses=len(records),
                         genotypes_preserved=sum(r['original_genotype'] for r in records),
                         reference_blocks_preserved=len(records),armed_houses=sum(r['armed'] for r in records),
                         women_taller=sum(r['female_cm']>r['male_cm'] for r in records)),ensure_ascii=False))

if __name__ == '__main__':
    main()
