"""Stage or apply the six author-approved phenotype changes with source checks."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import re
import shutil
from build_house_prompts import ROOT as POL, WORK, sections

VAULT=POL.parent
PLAN=json.loads((WORK/'cambios_apariencia_casas.json').read_text(encoding='utf-8'))
STAGE=WORK/'revision_apariencia_casas'
MANIFEST=STAGE/'manifest.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def replace_section(text,heading,body):
    pattern=r'(^## '+re.escape(heading)+r'[ \t]*\n)(.*?)(?=^## |\Z)'
    result,n=re.subn(pattern,lambda m:m.group(1)+'\n'+body.strip()+'\n\n',text,count=1,flags=re.M|re.S)
    assert n==1,heading
    return result

def replace_profile_lead(block,hair,eyes):
    first,*tail=block.split('\n\n')
    parts=first.split(';')
    assert len(parts)>=3 and 'ojos' in parts[1].casefold(),first
    parts[0]='Cabello '+hair
    parts[1]=' ojos '+eyes
    return ';'.join(parts)+(''.join('\n\n'+t for t in tail))

def stage():
    STAGE.mkdir(exist_ok=True)
    changes={}
    original={}
    old_blocks={}
    new_blocks={}
    for item in PLAN['selected']:
        path=Path(item['path'])
        raw=path.read_bytes()
        assert sha(raw)==item['original_sha256'],f'La ficha cambió después del sorteo: {path.name}'
        text=raw.decode('utf-8-sig').replace('\r\n','\n')
        data=sections(text)
        old=data['Perfil fenotípico canónico']
        new=replace_profile_lead(old,item['hair'],item['eyes'])
        old_blocks[item['name']]=old
        new_blocks[item['name']]=new
        revised=replace_section(text,'Perfil fenotípico canónico',new)
        assert sections(revised)['Referencias genéticas orientativas']==data['Referencias genéticas orientativas']
        assert sections(revised).get('Genotipo poblacional orientativo')==data.get('Genotipo poblacional orientativo')
        changes[path]=revised
        original[path]=raw
    profiles=POL/'Perfil Fenotípico'
    for name,items in [('Casas Mayores.md',[x for x in PLAN['selected'] if x['category']=='Casas Mayores']),
                       ('Casas Menores.md',[x for x in PLAN['selected'] if x['category']=='Casas Menores'])]:
        path=profiles/name
        original[path]=path.read_bytes()
        text=original[path].decode('utf-8-sig').replace('\r\n','\n')
        for item in items:
            heading=re.search(r'^## (?:\d+|M-\d+)\. Casa '+re.escape(item['name'])+r'$',text,re.M)
            assert heading,item['name']
            text=replace_section(text,heading.group(0)[3:],new_blocks[item['name']])
        changes[path]=text
    path=profiles/'Perfil Fenotípico del reino.md'
    original[path]=path.read_bytes()
    text=original[path].decode('utf-8-sig').replace('\r\n','\n')
    for item in PLAN['selected']:
        name=item['name']
        profile=new_blocks[name].split('\n\n')[0].replace(';',',')
        if item['category']=='Casas Mayores':
            pattern=r'^\| '+re.escape(name)+r' \|[^\n]*$'
            replacement=f'| {name} | {profile} |'
        else:
            pattern=r'^(\| M-\d+ \| '+re.escape(name)+r' \|[^|]+\|)[^\n]*$'
            replacement=lambda m,profile=profile:m.group(1)+' '+profile+' |'
        text,n=re.subn(pattern,replacement,text,flags=re.M)
        assert n==1,name
    minor_names=', '.join(x['name'] for x in PLAN['selected'] if x['category']=='Casas Menores')
    major_names=', '.join(x['name'] for x in PLAN['selected'] if x['category']=='Casas Mayores')
    text=text.replace('cabello rubio claro, ceniza o dorado; ojos azules, celestes o gris azulados;',
                      f'cabello rubio claro, ceniza o dorado, con cabello castaño claro y ojos verdes en {minor_names}; ojos de tonalidad variable según cada ficha;')
    changes[path]=text
    # Keep the two active canonical Markdown sources consistent with the profiles.
    rule=(f'Las Casas Menores {minor_names} se representan con cabello castaño claro y ojos verdes. '
          f'Las Casas Mayores {major_names} se representan con cabello pelirrojo y ojos celestes. '
          'Son tendencias familiares humanas, con variación interna; no rasgos exclusivos ni genotipos obligatorios. '
          'La selección excluye las Casas con imágenes ya disponibles. La piel, pecas, textura capilar, '
          'complexión, heráldica y función conservan lo indicado en cada ficha.')
    for path in [WORK/'Canon V16 Maestro.md',VAULT/'00_Canon'/'Canon V16 Maestro.md']:
        original[path]=path.read_bytes()
        text=original[path].decode('utf-8-sig').replace('\r\n','\n')
        for item in PLAN['selected']:
            if item['category']=='Casas Mayores':
                pattern=r'^- \*\*'+re.escape(item['name'])+r':\*\*[^\n]*$'
                text=re.sub(pattern,lambda m,item=item:f'- **{item["name"]}:** '+new_blocks[item['name']].split('\n\n')[0],text,flags=re.M)
        text=text.replace('cabello rubio claro, ceniza o dorado; ojos azules, celestes o gris azulados;',
                          f'cabello rubio claro, ceniza o dorado; {minor_names} presentan cabello castaño claro y ojos verdes; ojos de tonalidad variable según cada ficha;')
        text+='\n\n## Variación fenotípica adoptada para seis Casas\n\n'+rule+'\n'
        changes[path]=text
    path=VAULT/'00_Canon'/'Registro de Cambios.md'
    original[path]=path.read_bytes()
    text=original[path].decode('utf-8-sig').replace('\r\n','\n')
    text+='\n- Revisión visual de las Casas: '+rule+' Se recupera el orden anterior del catálogo de prompts.\n'
    changes[path]=text
    manifest=[]
    for i,(path,text) in enumerate(changes.items()):
        dest=STAGE/f'{i:02d}.md'
        dest.write_text(text,encoding='utf-8')
        manifest.append(dict(target=str(path),stage=str(dest),old_sha256=sha(original[path]),new_sha256=sha(dest.read_bytes())))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(files_staged=len(manifest),minor=minor_names,major=major_names),ensure_ascii=False))

def apply():
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    images=[p for p in (VAULT/'07_Imagenes').rglob('*') if p.is_file()]
    for item in PLAN['selected']:
        path=Path(item['path'])
        assert not any(im.stem==path.stem or im.stem.startswith(path.stem+' ') for im in images),f'Imagen nueva detectada para {item["name"]}'
        assert not re.search(r'!\[\[',path.read_text(encoding='utf-8-sig')),item['name']
    for entry in manifest:
        assert sha(Path(entry['target']).read_bytes())==entry['old_sha256'],entry['target']
    backup=STAGE/('respaldo-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    backup.mkdir()
    for i,entry in enumerate(manifest):
        target=Path(entry['target'])
        shutil.copy2(target,backup/f'{i:02d}-{target.name}')
        shutil.copyfile(entry['stage'],target)
        assert sha(target.read_bytes())==entry['new_sha256']
    print(json.dumps(dict(files_updated=len(manifest),backup=str(backup)),ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    apply() if args.apply else stage()
