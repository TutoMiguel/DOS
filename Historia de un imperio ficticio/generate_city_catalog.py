from pathlib import Path
ROOT=Path('obsidian_catalog_extra')

def make(path,title,body,kind='ciudad'):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f"---\ntipo: {kind}\ncanon: V16\nestado: vigente\necon03: incluida\n---\n\n# {title}\n\n{body}\n",encoding='utf-8')

provinces={
'Arnor Oriental':'Provincia de Arnor equivalente a Ontario. Entidad superior: [[../Entidades Politicas/Reinos Constituyentes/Aranath Valinor|Aranath Valinor]].',
'Cardolan':'Provincia de Arnor equivalente a Quebec. Su principal ciudad es Cardolan.',
'Forochel':'Provincia de Arnor equivalente a Labrador continental.',
'Arthedain':'Provincia de Arnor equivalente a Nueva Escocia.',
'Rhudaur':'Provincia de Arnor equivalente a Nuevo Brunswick y Maine.',
'Tolfalas':'Provincia de Arnor equivalente a Isla del Príncipe Eduardo.',
'Númenor':'Provincia insular de Arnor equivalente a Terranova.',
'Provincia de Guyana':'Provincia de Sírënandë equivalente a Guyana.',
'Provincia de Surinam':'Provincia de Sírënandë equivalente a Surinam.',
'Provincia de Guayana Oriental':'Provincia de Sírënandë equivalente a Guayana Francesa.',
'Rhunost':'Provincia autónoma interna de Harnen, equivalente a Musandam. No es unidad federal separada.'}
for n,b in provinces.items(): make(Path('02_Geografia/Provincias')/(n+'.md'),n,b,'provincia')

groups={
'Arnor': [('Annúminas','Toronto','capital provincial; 20 M urbanos'),('Fornost','Montreal','ciudad principal'),('Cardolan','Quebec','ciudad principal'),('Amon Sûl','Ottawa','ciudad principal'),('Hithlum','Halifax','ciudad principal'),('Rhûn','Saint John','ciudad principal'),('Etten','Labrador City','ciudad principal'),('Bree','Portland','ciudad principal'),('Tolfalas','Charlottetown','ciudad principal'),('Hamilton','Hamilton','ciudad principal de Ontario'),('Tyrn Gorthad','Kingston','ciudad principal'),('Emyn Uial','Thunder Bay','ciudad principal'),('Calenhad','Windsor','ciudad principal')],
'Calenardhon Austral': [('Pelargir Austral','Porto Alegre','capital administrativa propuesta'),('Calenport','Florianópolis','ciudad principal'),('Rómenna Austral','Rio Grande','ciudad principal'),('Esgaroth Austral','Pelotas','ciudad principal'),('Dol Amroth Austral','Joinville','ciudad principal'),('Barad Calen','Caxias do Sul','ciudad principal'),('Minas Tirith Austral','Santa Maria','ciudad principal'),('Osgiliath del Sur','Passo Fundo','ciudad principal'),('Edhellond Austral','Itajaí','ciudad principal'),('Forlond Austral','São José do Norte','ciudad principal'),('Calenost','Chapecó','ciudad principal')],
'Sírënandë': [('Sirion','Georgetown','capital administrativa propuesta'),('Erellond Sur','Paramaribo','ciudad principal'),('Calasir','Cayena','ciudad principal'),('Demerion','New Amsterdam','ciudad principal'),('Kourondë','Kourou','ciudad principal'),('Eldalondë Oriental','Saint-Laurent-du-Maroni','ciudad principal'),('Sarnath','Lelydorp','ciudad principal'),('Rómennar','Moengo','ciudad principal'),('Barad Calen','Matoury','ciudad principal'),('Amon Rûdh Oriental','Remire-Montjoly','ciudad principal'),('Esequielond','Bartica','ciudad principal'),('Calenport Sur','Albina','ciudad principal')],
'Caribe del Reino': [('Harlond Sur','Puerto España','capital administrativa propuesta de Trinidad'),('Dol Amroth Menel','Scarborough','capital administrativa propuesta de Tobago'),('Eryn Lasgalen','Nassau','capital administrativa propuesta de Bahamas'),('Tol Galen','Hamilton','capital administrativa propuesta de Bermudas'),('Lond Daer','Bridgetown','capital administrativa propuesta de Barbados')],
'Entidades del Reino': [('Vinyamar','Barranquilla','capital de Colombia Costera'),('Tirion del Istmo','Ciudad de Panamá','capital administrativa propuesta de Panamá Federal'),('Tirith Anor','Caracas','capital administrativa propuesta de Venezuela Federal'),('Barad Oron','Puerto Ordaz','capital administrativa propuesta de Provincia del Orinoco'),('Eressëa Menel','Las Palmas','capital administrativa propuesta de Nosselië Toliva')]
}
for group,items in groups.items():
 for n,real,role in items:
  make(Path('04_Mapa Politico/Ciudades')/(n+'.md'),n,f'Equivalencia: {real}. Territorio o grupo: {group}. Función: {role}. Su población y producción están incluidas en la cuenta ECON-03 de su entidad superior y no se suman aparte.')

make(Path('04_Mapa Politico/Ciudades/Índice Urbano V16.md'),'Índice Urbano V16','''Este índice reúne las ciudades principales y capitales del ámbito Federación más Protectorados. Cada ciudad está incluida en la población y cuenta ECON-03 de su territorio superior. Las capitales marcadas como propuestas no modifican el canon hasta su confirmación.''','indice urbano')
