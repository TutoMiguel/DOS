from pathlib import Path

ROOT = Path('obsidian_catalog')

def note(path, title, body, status='vigente'):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\ntipo: entidad territorial\nestado_canonico: {status}\ncanon: V16\n---\n\n# {title}\n\n{body}\n", encoding='utf-8')

note('00_Indice Territorial/Índice Territorial V16.md', 'Índice Territorial V16', '''Este catálogo cubre hasta la Federación Gwaith Valinor y los protectorados de Beleg Valinor. No incluye los aliados soberanos de Gwaith Aear.

## Jerarquía

- [[../02_Geografia/Entidades Politicas/Reinos Constituyentes/Aranath Valinor|Aranath Valinor]]
- [[../02_Geografia/Entidades Politicas/Federacion Directa/Gwaith Valinor|Gwaith Valinor]]
- [[../02_Geografia/Entidades Politicas/Protectorados/Beleg Valinor|Beleg Valinor]]

## Catálogos

- [[../02_Geografia/Entidades Politicas/Índice de Entidades Políticas]]
- [[../02_Geografia/Provincias/Índice de Provincias]]
- [[../02_Geografia/Regiones/Índice de Regiones]]
- [[../02_Geografia/Paises y Estados de Referencia/Índice de Países y Estados]]
- [[../04_Mapa Politico/Ciudades/Índice de Ciudades]]''')

note('02_Geografia/Entidades Politicas/Índice de Entidades Políticas.md', 'Índice de Entidades Políticas', '''## Reino constituyente

- [[Reinos Constituyentes/Aranath Valinor]]

## Federación

- [[Federacion Directa/Gwaith Valinor]]
- [[Federacion Directa/Malaca]]
- [[Federacion Directa/Hawái]]
- [[Federacion Directa/Fiyi]]
- [[Federacion Directa/Polinesia]]
- [[Federacion Directa/Micronesia]]
- [[Federacion Directa/Eryndor]]

## Protectorados

- [[Protectorados/Beleg Valinor]]
- [[Protectorados/Harnen]]
- [[Protectorados/Kheled-zâram]]
- [[Protectorados/Círdan]]
- [[Protectorados/Harlond]]
- [[Protectorados/Amon Rûdh]]
- [[Protectorados/Alqualondë]]
- [[Protectorados/Eglarest]]
- [[Protectorados/Pelargir]]

Los aliados de Gwaith Aear quedan fuera de este catálogo.''')

note('02_Geografia/Entidades Politicas/Reinos Constituyentes/Aranath Valinor.md', 'Aranath Valinor', 'Reino constituyente de [[../Federacion Directa/Gwaith Valinor|Gwaith Valinor]]. Incluye el núcleo insular y los territorios directos del Reino. Población: 481 millones. PIB PPA central: 58,50 billones.')
note('02_Geografia/Entidades Politicas/Federacion Directa/Gwaith Valinor.md', 'Gwaith Valinor', 'Federación soberana. Comprende [[../Reinos Constituyentes/Aranath Valinor|Aranath Valinor]] y las unidades federales directas. Población: 518 millones. PIB PPA operativo: 64,55 billones. Urbanización: 89,6 %.')
for name, body in {
    'Malaca':'Unidad federal directa. Península malaya y Singapur como distrito portuario integrado. Capital propuesta: Kuala Lumpur.',
    'Hawái':'Unidad federal directa. Archipiélago hawaiano. Capital propuesta: Honolulu.',
    'Fiyi':'Unidad federal directa. Archipiélago completo. Capital propuesta: Suva.',
    'Polinesia':'Unidad federal directa. Incluye Samoa, Tonga, Islas Cook, Polinesia Francesa, Wallis y Futuna, Tuvalu, Niue, Tokelau y Samoa Americana. Capital operativa propuesta: Papeete.',
    'Micronesia':'Unidad federal directa. Incluye Guam, Marianas del Norte, Palaos, Estados Federados de Micronesia, Marshall y Kiribati. Capital operativa propuesta: Hagåtña.',
    'Eryndor':'Unidad federal directa equivalente al archipiélago de Baréin. Capital: Manama. Población: 2 millones. PIB PPA: 0,18 billones.'}.items():
    note(f'02_Geografia/Entidades Politicas/Federacion Directa/{name}.md', name, body)

note('02_Geografia/Entidades Politicas/Protectorados/Beleg Valinor.md', 'Beleg Valinor', 'Gran Valinor: [[../Federacion Directa/Gwaith Valinor|Gwaith Valinor]] más protectorados y enclaves. Este catálogo incluye Harnen, Kheled-zâram, Círdan, Harlond, Amon Rûdh, Alqualondë, Eglarest y Pelargir.')
for name, body in {
    'Harnen':'Protectorado de Beleg Valinor, equivalente a Omán. Rhunost/Musandam es provincia autónoma interna. Capital propuesta: Muscat. Población: 8 millones. PIB PPA: 0,52 billones.',
    'Kheled-zâram':'Protectorado equivalente a Kuwait. Capital propuesta: Kuwait.',
    'Círdan':'Protectorado equivalente a Socotra. Capital propuesta: Hadibu.',
    'Harlond':'Protectorado equivalente a Adén. Capital propuesta: Adén.',
    'Amon Rûdh':'Protectorado equivalente a Yibuti. Capital propuesta: Yibuti.',
    'Alqualondë':'Protectorado equivalente a Chipre. Capital administrativa propuesta: Nicosia.',
    'Eglarest':'Protectorado equivalente a Malta. Capital propuesta: La Valeta.',
    'Pelargir':'Protectorado equivalente al enclave de Alejandría. Capital propuesta: Alejandría.'}.items():
    note(f'02_Geografia/Entidades Politicas/Protectorados/{name}.md', name, body, 'vigente/provisional')

provinces = {
    'Arnor Oriental':'Provincia de Arnor equivalente a Ontario.', 'Cardolan':'Provincia de Arnor equivalente a Quebec.',
    'Forochel':'Provincia de Arnor equivalente a Labrador continental.', 'Arthedain':'Provincia de Arnor equivalente a Nueva Escocia.',
    'Rhudaur':'Provincia de Arnor equivalente a Nuevo Brunswick y Maine.', 'Tolfalas':'Provincia de Arnor equivalente a Isla del Príncipe Eduardo.',
    'Númenor':'Provincia insular de Arnor equivalente a Terranova.', 'Provincia de Guyana':'Provincia de Sírënandë.',
    'Provincia de Surinam':'Provincia de Sírënandë.', 'Provincia de Guayana Oriental':'Provincia de Sírënandë.',
    'Rhunost':'Provincia autónoma interna de Harnen, equivalente a Musandam.'}
for name, body in provinces.items(): note(f'02_Geografia/Provincias/{name}.md', name, body)

regions = {
    'Valinor a Tyl':'Núcleo insular formado por Valinor, Tol Eressëa y Systreyjar.',
    'Valinor':'Territorio histórico del núcleo insular. Capital: [[../../04_Mapa Politico/Capitales/Nueva Tirion|Nueva Tirion]].',
    'Tol Eressëa':'Territorio insular del núcleo. Capital: [[../../04_Mapa Politico/Capitales/Avallónë|Avallónë]].',
    'Systreyjar':'Territorio insular del núcleo. Capital operativa propuesta: Taur-en-Mor.',
    'Calenardhon Austral':'Región del Reino equivalente a Rio Grande do Sul y Santa Catarina. Capital operativa propuesta: Pelargir Austral.',
    'Sírënandë':'Región del Reino formada por Guyana, Surinam y Guayana Francesa. Capital operativa propuesta: Sirion.',
    'Colombia Costera':'Región del Reino formada por 22 departamentos y Bogotá D.C. Capital: Vinyamar.',
    'Panamá Federal':'Territorio del Reino equivalente a Panamá. Capital operativa propuesta: Tirion del Istmo.',
    'Venezuela Federal':'Territorio del Reino. Capital operativa propuesta: Tirion Federal.',
    'Provincia del Orinoco':'Región transfronteriza del Reino. Capital operativa propuesta: Puerto Ordaz.',
    'Nosselië Toliva':'Archipiélago equivalente a Canarias. Capital operativa propuesta: Eressëa.',
    'Caribe del Reino':'Conjunto de Trinidad, Tobago, Bahamas, Bermudas y Barbados.'}
for name, body in regions.items(): note(f'02_Geografia/Regiones/{name}.md', name, body, 'vigente/provisional')

countries = ['Ontario','Quebec','Labrador','Nueva Escocia','Nuevo Brunswick','Maine','Isla del Príncipe Eduardo','Terranova','Guyana','Surinam','Guayana Francesa','Brasil','Malasia','Singapur','Baréin','Omán','Kuwait','Yibuti','Chipre','Malta','Egipto','Colombia','Panamá','Venezuela','Trinidad y Tobago','Bahamas','Bermudas','Barbados']
for name in countries: note(f'02_Geografia/Paises y Estados de Referencia/{name}.md', name, f'Entidad geográfica de referencia utilizada por el canon para delimitar territorios ficticios. [[../../00_Indice Territorial/Índice Territorial V16|Índice Territorial V16]]', 'referencia')

cities = {
    'Nueva Tirion':'Capital de Valinor. Población: 6,50 millones. Coordenadas: 30,10° N, 38,00° O.',
    'Avallónë':'Capital de Tol Eressëa y puerto principal. Coordenadas: 35,75° N, 42,35° O.',
    'Eldalondë':'Ciudad principal secundaria de Tol Eressëa. Población: 2,80 millones.',
    'Taur-en-Mor':'Centro urbano principal de Systreyjar. Población: 3,10 millones.',
    'Annúminas':'Capital provincial de Arnor, equivalente a Toronto. Población urbana: 20 millones.',
    'Vinyamar':'Capital administrativa de Colombia Costera.', 'Manama':'Capital de Eryndor.', 'Muscat':'Capital propuesta de Harnen.',
    'Kuala Lumpur':'Capital propuesta de Malaca.', 'Honolulu':'Capital propuesta de Hawái.', 'Suva':'Capital propuesta de Fiyi.',
    'Papeete':'Capital operativa propuesta de Polinesia.', 'Hagåtña':'Capital operativa propuesta de Micronesia.',
    'Kuwait':'Capital propuesta de Kheled-zâram.', 'Hadibu':'Capital propuesta de Círdan.', 'Adén':'Capital propuesta de Harlond.',
    'Yibuti':'Capital propuesta de Amon Rûdh.', 'Nicosia':'Capital administrativa propuesta de Alqualondë.', 'La Valeta':'Capital propuesta de Eglarest.',
    'Alejandría':'Capital propuesta de Pelargir.', 'Pelargir Austral':'Capital operativa propuesta de Calenardhon Austral.',
    'Sirion':'Capital operativa propuesta de Sírënandë.', 'Tirion del Istmo':'Capital operativa propuesta de Panamá Federal.',
    'Tirion Federal':'Capital operativa propuesta de Venezuela Federal.', 'Puerto Ordaz':'Capital operativa propuesta de Provincia del Orinoco.',
    'Eressëa':'Capital operativa propuesta de Nosselië Toliva.', 'Puerto España':'Capital de Trinidad.', 'Scarborough':'Capital de Tobago.',
    'Nassau':'Capital de Bahamas.', 'Hamilton':'Capital de Bermudas.', 'Bridgetown':'Capital de Barbados.'}
for name, body in cities.items(): note(f'04_Mapa Politico/Ciudades/{name}.md', name, body, 'vigente/provisional')

note('04_Mapa Politico/Ciudades/Índice de Ciudades.md', 'Índice de Ciudades', '''Este índice reúne capitales, ciudades principales y capitales operativas del ámbito Federación más Protectorados.

La etiqueta `vigente/provisional` distingue las capitales explícitamente fijadas de las propuestas derivadas de la información disponible.''')
