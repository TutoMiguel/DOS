from pathlib import Path

ROOT=Path('house_catalog')

houses=[
('Noldor','Casa Noldor','Noldor','Pericia, memoria y fuego creador','Noldor, i ndim i naur','Casa de eruditos, artesanos y guardianes de archivos.'),
('Vanyar','Casa Vanyar','Vanyar','Luz, disciplina y concordia','Calad, thalion, hain','Casa de tradición sacerdotal y diplomática.'),
('Teleri','Casa Teleri','Teleri','Mares, canto y navegación','Beleg aer, linnathon','Casa marítima vinculada a puertos y astilleros.'),
('Elwing','Casa Elwing','Elwing','Esperanza sobre las aguas','Estel or aer','Casa de navegantes, embajadores y cartógrafos.'),
('Círdan','Casa Círdan','Círdan','Construimos para los que parten','Tirith i cemen, ceven','Casa naval y de constructores de naves.'),
('Mithlond','Casa Mithlond','Mithlond','Los puertos unen los reinos','Mithlond athan i aer','Casa mercantil y portuaria.'),
('Esgal','Casa Esgal','Esgal','La sombra protege la frontera','Esgal na guruth','Casa de inteligencia, exploración y vigilancia.'),
('Calenhad','Casa Calenhad','Calenhad','La luz guía el camino','Calad tiria i râd','Casa de ingenieros, caminos y fortificaciones.'),
('Fornost','Casa Fornost','Fornost','La piedra recuerda','Gond na thûl','Casa de juristas, arquitectos y administradores.'),
('Annúminas','Casa Annúminas','Annúminas','El lago guarda la corona','Nen dorthad i aran','Casa lacustre de gobierno provincial.'),
('Alqualondë','Casa Alqualondë','Alqualondë','El mar canta en nuestras velas','Aear linnatha veleth','Casa de armadores y navegantes del núcleo insular.'),
('Armenelos','Casa Armenelos','Armenelos','La altura contempla el reino','Târ menel cenatha','Casa de magistrados y observatorios.'),
('Eldalondë','Casa Eldalondë','Eldalondë','La memoria vive en la costa','Remb i falas','Casa de historiadores y custodios de Tol Eressëa.'),
('Taur-en-Mor','Casa Taur-en-Mor','Taur-en-Mor','La isla resiste al viento','Tol thalion na gwaew','Casa de Systreyjar y de sus flotas septentrionales.'),
('Barad Calen','Casa Barad Calen','Barad Calen','La torre vigila el sur','Barad tiria i angren','Casa austral de defensa y metalurgia.'),
('Dol Amroth','Casa Dol Amroth','Dol Amroth','Honor junto al mar','Aegas naer aear','Casa de diplomacia costera y caballería naval.'),
('Pelargir','Casa Pelargir','Pelargir','Los ríos conducen al mundo','Sir i ven, sir i aer','Casa de comercio fluvial y administración portuaria.'),
('Harlond','Casa Harlond','Harlond','El puerto abre las puertas','And i hûl, and i aer','Casa de logística y relaciones exteriores.'),
('Minas Anor','Casa Minas Anor','Minas Anor','La llama no se extingue','Naur ú-dhartha','Casa de energía, ciencia y defensa.'),
('Eryn Lasgalen','Casa Eryn Lasgalen','Eryn Lasgalen','El bosque alimenta al reino','Taur givatha i ardhon','Casa de agricultura, madera y conservación.'),
('Rhunost','Casa Rhunost','Rhunost','El estrecho escucha','Cirith lasta','Casa oriental de vigilancia y seguridad marítima.'),
('Harnost','Casa Harnost','Harnost','La arena guarda la riqueza','Aren dorthad i mâl','Casa de comercio energético y protectorados orientales.'),
('Eressëa Menel','Casa Eressëa Menel','Eressëa Menel','Las islas miran al cielo','Tolthas cenatha menel','Casa atlántica de observatorios y comunicaciones.'),
('Calenor','Casa Calenor','Calenor','El verde renace','Calen obnovatha','Casa de sanadores, jardines y biotecnología.'),
('Telcontar','Casa Telcontar','Telcontar','El heredero sirve al reino','I thain aran','Casa Real; extra número 25. Ariadna Telcontar pertenece a esta casa.')]

lines=['---','tipo: indice nobiliario','canon: V16','fecha: 833dc','---','','# Las 25 Casas de Valinari','','El orden comprende 24 casas nobles y la Casa Telcontar como Casa Real extra número 25.','']
for i,(slug,title,token,motto,trans,desc) in enumerate(houses,1):
    royal = 'Casa Real' if slug=='Telcontar' else 'Casa noble'
    body=f'''---\ntipo: casa noble\nnumero: {i if slug != "Telcontar" else 25}\nestatus: {royal}\nfecha_referencia: 833dc\ncanon: V16\n---\n\n# {title}\n\n**Estatus:** {royal}.\n\n{desc}\n\n## Blasón\n\n- Campo: diseño heráldico pendiente de ilustración final.\n- Emblema: {token}.\n- Colores: se definirán en la carta heráldica visual sin alterar el emblema textual.\n\n## Estandarte\n\nEstandarte vertical con el emblema de la casa, pensado para corte, fortaleza y ceremonia.\n\n## Lema\n\n- Sindarin: **{motto}**\n- Glosa: lema de la casa asociado a {token}.\n- Transcripción para alto tengwar: **{trans}**\n\n## Relaciones\n\n- [[../Índice de Casas Nobles]]\n- [[../../00_Canon/Canon V16 Maestro|Canon V16 Maestro]]\n- [[../../09_Politica/Índice Político Institucional|Índice Político Institucional]]\n'''
    p=ROOT/'09_Politica'/(title+'.md'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body,encoding='utf-8')
    lines.append(f'{i if slug != "Telcontar" else 25}. [[09_Politica/{title}|{title}]] — {royal}')
(ROOT/'09_Politica/Índice de Casas Nobles.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

chars={
'Don Esteban de ValinARI.md':'''---\ntipo: personaje\nrol: patriarca de la Casa Telcontar\nfecha_referencia: 833dc\ncanon: V16\n---\n\n# Don Esteban de ValinARI\n\nPatriarca de [[Casa Telcontar]] y padre de [[Ariadna]]. Participa en la corte de Nueva Tirion y en el Consejo de Nobles.\n\n- Casa: [[Casa Telcontar]]\n- Residencia: [[../04_Mapa Politico/Capitales/Nueva Tirion|Nueva Tirion]]\n''',
'Doña Marina de ValinARI.md':'''---\ntipo: personaje\nrol: matriarca de la Casa Telcontar\nfecha_referencia: 833dc\ncanon: V16\n---\n\n# Doña Marina de ValinARI\n\nMatriarca de [[Casa Telcontar]] y madre de [[Ariadna]]. Su influencia se relaciona con la educación, la diplomacia cortesana y las redes familiares de Nueva Tirion.\n\n- Casa: [[Casa Telcontar]]\n- Residencia: [[../04_Mapa Politico/Capitales/Nueva Tirion|Nueva Tirion]]\n''',
'Ëarendil y Elwing Noldor.md':'''---\ntipo: personajes\nrol: linaje histórico de la Casa Noldor\nfecha_referencia: 833dc\ncanon: V16\n---\n\n# Ëarendil y Elwing Noldor\n\nPareja y linaje histórico asociado a [[Casa Noldor]]. Su memoria se conserva dentro de la genealogía noble y las tradiciones marítimas de Valinari.\n\n- Casa: [[Casa Noldor]]\n- Relación: tradición ancestral y legitimidad histórica.\n'''}
for name,body in chars.items():
 p=ROOT/'03_Personajes'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body,encoding='utf-8')

(ROOT/'09_Politica/Índice Político Institucional.md').write_text('''---\ntipo: indice politico\ncanon: V16\nfecha_referencia: 833dc\n---\n\n# Índice Político Institucional\n\n- [[Índice de Casas Nobles]]\n- [[Casa Telcontar]]\n- [[../../00_Canon/Matriz de Estatus Político|Matriz de Estatus Político]]\n- [[../../04_Mapa Politico/Índice Político|Índice Político Territorial]]\n''',encoding='utf-8')
(ROOT/'03_Personajes/Índice de Personajes.md').write_text('''---\ntipo: indice de personajes\ncanon: V16\nfecha_referencia: 833dc\n---\n\n# Índice de Personajes\n\n## Casa Telcontar\n\n- [[Ariadna]]\n- [[Don Esteban de ValinARI]]\n- [[Doña Marina de ValinARI]]\n\n## Casa Noldor\n\n- [[Ëarendil y Elwing Noldor]]\n\nLas casas nobles se organizan en [[../09_Politica/Índice de Casas Nobles|Índice de Casas Nobles]].\n''',encoding='utf-8')
