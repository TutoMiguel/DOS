"""Record, stage, apply and audit the adopted individual hair distribution."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
from build_house_prompts import ROOT, WORK, houses, sections

VAULT=ROOT.parent
STAGE=WORK/'consolidacion_capilar_casas'
PLAN=STAGE/'sorteo.json'
MANIFEST=STAGE/'manifest.json'
TITLE='Registro de representantes de las Casas'
HEADING='Variación fenotípica y representantes de las Casas'
WHITE='rubio platinado blanco'
COMMON=['rubio claro','rubio ceniza','rubio dorado','rubio muy claro','rubio oscuro']

def read(p):return p.read_text(encoding='utf-8-sig')
def sha(b):return hashlib.sha256(b).hexdigest()

def resolve_hair(profile):
    first=profile.split(';')[0].casefold()
    for color in ['castaño claro','rubio platino','rubio muy claro','rubio ceniza','rubio dorado','rubio oscuro','rubio claro']:
        if color in first:return color
    raise ValueError(first)

def draw():
    catalog=houses()
    eligible=[h for h in catalog if h['category'] in ('Casa Menor','Casa Vasalla')]
    for h in eligible:
        assert not re.search(r'!\[\[',h['text']),h['name']
        assert not any(p.stem.startswith('Casa '+h['name']) for p in (VAULT/'07_Imagenes').iterdir() if p.is_file()),h['name']
    if PLAN.exists():return json.loads(read(PLAN))
    seed=random.SystemRandom().getrandbits(64)
    rng=random.Random(seed)
    minor=[h for h in eligible if h['category']=='Casa Menor']
    original=[resolve_hair(h['data']['Perfil fenotípico canónico']) for h in minor]
    browns=[i for i,x in enumerate(original) if x=='castaño claro']
    assert len(browns)==3
    replace=rng.sample(browns,2)
    male,female=original.copy(),original.copy()
    for i in replace:male[i]='pelirrojo'
    for i in rng.sample([i for i,x in enumerate(female) if x!='castaño claro'],3):female[i]='pelirrojo'
    rng.shuffle(male);rng.shuffle(female)
    allocation=[dict(name=h['name'],category=h['category'],male=m,female=f) for h,m,f in zip(minor,male,female)]
    vassal=[h for h in eligible if h['category']=='Casa Vasalla']
    male=['pelirrojo']*2+['castaño oscuro']+[WHITE]+[COMMON[i%len(COMMON)] for i in range(31)]
    female=['pelirrojo']*4+['castaño claro']*3+[WHITE]*2+[COMMON[i%len(COMMON)] for i in range(26)]
    assert len(male)==len(female)==len(vassal)==35
    rng.shuffle(male);rng.shuffle(female)
    allocation += [dict(name=h['name'],category=h['category'],male=m,female=f) for h,m,f in zip(vassal,male,female)]
    major=json.loads(read(WORK/'redistribucion_capilar_nueve_casas'/'sorteo.json'))
    plan=dict(seed=str(seed),algorithm='Permutaciones independientes por sexo de paletas con recuentos fijados; sin resorteo.',
              replaced_male_brown_source=[minor[i]['name'] for i in replace],
              white_split=dict(female=2,male=1),
              major_seed=major['seed'],
              allocation=[dict(x,category='Casa Mayor') for x in major['allocation']]+allocation)
    PLAN.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    return plan

def counts(plan):
    out={}
    for cat in ('Casa Mayor','Casa Menor','Casa Vasalla'):
        group=[x for x in plan['allocation'] if x['category']==cat]
        out[cat]=dict(houses=len(group),male=dict(Counter(x['male'] for x in group)),
                      female=dict(Counter(x['female'] for x in group)),
                      mixed_couples=sum(x['male']!=x['female'] for x in group))
    assert out['Casa Mayor']['houses']==9
    assert out['Casa Menor']['houses']==24 and out['Casa Vasalla']['houses']==35
    assert out['Casa Mayor']['male'].get('pelirrojo')==out['Casa Mayor']['female'].get('pelirrojo')==2
    m,v=out['Casa Menor'],out['Casa Vasalla']
    assert m['male'].get('pelirrojo')==2 and m['female'].get('pelirrojo')==3
    assert m['male'].get('castaño claro')==1 and m['female'].get('castaño claro')==3
    assert v['male'].get('pelirrojo')==2 and v['female'].get('pelirrojo')==4
    assert v['female'].get('castaño claro')==3 and v['male'].get('castaño oscuro')==1
    assert v['male'].get(WHITE)==1 and v['female'].get(WHITE)==2
    return out

def table(rows,prefix=''):
    folders={'Casa Mayor':'Casas Mayores','Casa Menor':'Casas Menores','Casa Vasalla':'Casas Vasallas'}
    lines=['| Casa | Cabello del hombre | Cabello de la mujer |','|---|---|---|']
    for x in rows:
        link=f'{prefix}{folders[x["category"]]}/Casa {x["name"]}'
        lines.append(f'| [[{link}|Casa {x["name"]}]] | {x["male"]} | {x["female"]} |')
    return '\n'.join(lines)

POLICY=('La galería representa parejas humanas adultas de la nobleza valinari. El color natural de cabello '
        'se asigna a cada cónyuge por separado y permite matrimonios entre personas de distinto color. '
        'Los perfiles familiares describen tendencias con variación interna; el reparto individual vigente '
        'prevalece al representar a estas parejas. Se conservan ojos, piel, pecas y textura capilar de la ficha, '
        'además de alturas, complexiones, cortes, barbas, posturas, posiciones, objetos de oficio y heráldica. '
        'Las referencias genéticas siguen siendo orientativas y poligénicas. El cabello platinado blanco '
        'es una descripción visual de pigmentación y no determina un diagnóstico de albinismo.')
SUMMARY=('Se conserva el sorteo de las nueve Casas Mayores pendientes: dos hombres y dos mujeres pelirrojos, '
         'siete hombres y siete mujeres de tonos rubios habituales. En las 24 Casas Menores hay tres mujeres '
         'y dos hombres pelirrojos; los dos hombres reemplazan dos de los tres casos castaño claro del reparto '
         'anterior, quedando un hombre y tres mujeres castaño claro. En las 35 Casas Vasallas se asignan cuatro '
         'mujeres y dos hombres pelirrojos, tres mujeres castaño claro, un hombre castaño oscuro y tres '
         'representantes de cabello rubio platinado blanco, dos mujeres y un hombre. Los demás representantes '
         'conservan tonos rubios habituales.')

def canon_section(plan,prefix='09_Politica/'):
    parts=['## '+HEADING,'',POLICY,'',SUMMARY,'',
           'Los perfiles familiares de Hallas, Thoron y Angren mantienen su referencia castaño claro y ojos verdes; '
           'los de Fornost, Harnost y Mithlond mantienen sus tendencias pelirrojas y ojos celestes. '
           'El color de cabello de cada representante sigue la asignación individual de las tablas. '
           'Las quince Casas Mayores ya ilustradas y la Casa Real conservan su representación previa.','']
    for cat,title in [('Casa Mayor','Casas Mayores pendientes de imagen'),('Casa Menor','Casas Menores'),('Casa Vasalla','Casas Vasallas')]:
        parts+=['### '+title,'',table([x for x in plan['allocation'] if x['category']==cat],prefix),'']
    return '\n'.join(parts)

def stage():
    STAGE.mkdir(exist_ok=True)
    plan=draw();summary=counts(plan)
    changes={};catalog={h['name']:h for h in houses()}
    for x in plan['allocation']:
        if x['category']=='Casa Mayor':continue
        h=catalog[x['name']];text=h['text']
        block=('## Representantes de la galería\n\nPareja adulta anónima para la imagen individual de esta Casa.\n\n'
               f'- **Cabello del hombre:** {x["male"]}\n- **Cabello de la mujer:** {x["female"]}\n\n'
               'El color capilar se fija por individuo. Los cónyuges pueden tener distinto color natural de cabello. '
               'El perfil familiar admite variación y matrimonios entre linajes; se conservan ojos, piel, pecas, '
               'textura capilar y las demás decisiones visuales de la ficha.\n\n'
               f'[[../{TITLE}|Registro vigente de representantes]].\n\n')
        if '## Representantes de la galería' in text:
            text=re.sub(r'(?ms)^## Representantes de la galería\n.*?(?=^## |\Z)',lambda _:block,text,count=1)
        else:text=text.replace('## Personajes asociados',block+'## Personajes asociados',1)
        for key in ('Perfil fenotípico canónico','Genotipo poblacional orientativo','Referencias genéticas orientativas'):
            assert sections(text).get(key)==h['data'].get(key),(h['name'],key)
        changes[h['path']]=text
    registry=('---\ntipo: registro visual\ncanon: V16\ncasas_con_reparto_individual: 68\nrepresentantes: 136\n---\n'
              '# '+TITLE+'\n\n'+POLICY+'\n\n'+SUMMARY+'\n\n')
    for cat,label in [('Casa Mayor','Casas Mayores pendientes de imagen'),('Casa Menor','Casas Menores'),('Casa Vasalla','Casas Vasallas')]:
        registry+='## '+label+'\n\n'+table([x for x in plan['allocation'] if x['category']==cat])+'\n\n'
    registry+=('## Registro del sorteo\n\n'+f'Semilla de Menores y Vasallas: {plan["seed"]}. {plan["algorithm"]} '
               f'Semilla conservada de Mayores: {plan["major_seed"]}.\n\n'
               '## Referencias relacionadas\n\n- [[Prompts Visuales de las 84 Casas]]\n'
               '- [[Perfil Fenotípico/Perfil Fenotípico del reino]]\n- [[Índice de Casas Nobles]]\n'
               '- [[../00_Canon/Canon V16 Maestro|Canon V16 Maestro]]\n')
    changes[ROOT/(TITLE+'.md')]=registry
    for folder,cat in [('Casas Mayores','Casa Mayor'),('Casas Menores','Casa Menor'),('Casas Vasallas','Casa Vasalla')]:
        p=ROOT/'Perfil Fenotípico'/(folder+'.md');text=read(p)
        text=re.sub(r'(?ms)\n## Colores individuales de la galería\n.*?(?=^## |\Z)','\n',text)
        text+='\n\n## Reparto individual vigente\n\n'+POLICY+'\n\n'+table([x for x in plan['allocation'] if x['category']==cat],'../')+'\n'
        changes[p]=text
    p=ROOT/'Perfil Fenotípico'/'Perfil Fenotípico del reino.md';text=read(p)
    text=re.sub(r'(?ms)\n## Colores individuales de la galería\n.*?(?=^## |\Z)','\n',text)
    changes[p]=text+'\n\n## Reparto individual vigente\n\n'+POLICY+'\n\n'+SUMMARY+'\n\n'+f'[[../{TITLE}|Registro completo de las parejas y colores de cabello]].\n'
    for p in [WORK/'Canon V16 Maestro.md',VAULT/'00_Canon'/'Canon V16 Maestro.md']:
        text=read(p)
        assert '## Variación fenotípica adoptada para seis Casas' in text
        text=re.sub(r'(?ms)^## Variación fenotípica adoptada para seis Casas\n.*\Z',lambda _:canon_section(plan),text,count=1)
        changes[p]=text
    p=ROOT/'Distribución capilar de las nueve Casas Mayores pendientes.md';text=read(p)
    anchor='## Referencias relacionadas'
    text=text.replace(anchor,f'El reparto se conserva e integra en [[{TITLE}]], junto con Menores y Vasallas.\n\n'+anchor,1)
    changes[p]=text
    p=VAULT/'01_Cronologia'/'Cronología Territorial V16.md'
    changes[p]=read(p)+'\n\n## Referencia editorial de la galería nobiliaria\n\nEl registro visual de los linajes conserva la referencia narrativa '
    changes[p]+='de 833 d. C. Las asignaciones individuales de cabello y los matrimonios representados son decisiones de la galería; '
    changes[p]+='las fechas históricas y biográficas conservan su valor canónico. '+SUMMARY+'\n\n'
    changes[p]+=f'[[09_Politica/{TITLE}|Registro vigente de representantes de las Casas]].\n'
    p=VAULT/'00_Canon'/'Registro de Cambios.md'
    changes[p]=read(p)+'\n- Consolidación del reparto capilar individual de Mayores, Menores y Vasallas. '+SUMMARY+' '
    changes[p]+=f'Semilla de Menores y Vasallas: {plan["seed"]}. Se sincronizan fichas, perfiles, prompts y documentos maestros.\n'
    p=ROOT/'Auditoría de Prompts Visuales de las Casas.md'
    changes[p]=read(p)+'\n\n## Consolidación vigente de Mayores Menores y Vasallas\n\n'+SUMMARY+'\n\n'
    changes[p]+=f'[[{TITLE}|Registro completo y verificable del reparto]].\n'
    p=ROOT/'Índice de Casas Nobles.md'
    changes[p]=read(p)+'\n\n## Galería de representantes\n\n'+f'- [[{TITLE}|Reparto individual vigente de cabello por pareja]].\n'
    manifest=[]
    for i,(p,text) in enumerate(changes.items()):
        dest=STAGE/f'{i:02d}.md';dest.write_text(text,encoding='utf-8')
        manifest.append(dict(target=str(p),stage=str(dest),before=sha(p.read_bytes()) if p.exists() else None,after=sha(dest.read_bytes())))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (STAGE/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (STAGE/'seccion_canon.md').write_text(canon_section(plan),encoding='utf-8')
    print(json.dumps(dict(files=len(manifest),counts=summary,special=[x for x in plan['allocation'] if x['category']!='Casa Mayor' and any(c in [x['male'],x['female']] for c in ['pelirrojo','castaño claro','castaño oscuro',WHITE])]),ensure_ascii=False))

def apply():
    manifest=json.loads(read(MANIFEST));plan=json.loads(read(PLAN));counts(plan)
    for x in manifest:
        p=Path(x['target']);assert (sha(p.read_bytes()) if p.exists() else None)==x['before'],p
    backup=STAGE/('respaldo-'+datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
    for i,x in enumerate(manifest):
        p=Path(x['target'])
        if p.exists():shutil.copy2(p,backup/f'{i:02d}-{p.name}')
        shutil.copy2(x['stage'],p)
    target=ROOT/'Prompts Visuales de las 84 Casas.md';old=read(target)
    shutil.copy2(target,backup/target.name)
    assigned=WORK/'asignaciones_visuales_casas.json';shutil.copy2(assigned,backup/assigned.name)
    before=json.loads(read(assigned))
    subprocess.run([sys.executable,str(WORK/'build_house_prompts.py')],check=True,cwd=WORK)
    after=json.loads(read(assigned));new=read(WORK/'prompts_visuales_actualizados.md')
    def chunks(t):return {m.group(1):m.group(0).strip() for m in re.finditer(r'(?ms)^## Casa (.+?)\n.*?(?=^## Casa |^# Casa |\Z)',t)}
    a,b=chunks(old),chunks(new)
    changed={n for n in a if a[n]!=b[n]}
    expected={x['name'] for x in plan['allocation'] if x['category']!='Casa Mayor'}
    assert len(a)==len(b)==84 and list(a)==list(b) and changed==expected,(len(changed),changed^expected)
    for r,s in zip(before,after):
        for k in ('name','male_cm','female_cm','male_side','female_side','male_pose','female_pose','male_item','female_item','role','armed','visual_index'):
            assert r[k]==s[k],(r['name'],k)
    for x in plan['allocation']:
        r=next(r for r in after if r['name']==x['name'])
        assert (r['male_hair_color'],r['female_hair_color'])==(x['male'],x['female']),x
    for h in houses():
        for key in ('Referencias genéticas orientativas','Genotipo poblacional orientativo'):
            if h['data'].get(key):assert h['data'][key] in b[h['name']],(h['name'],key)
    shutil.copy2(WORK/'prompts_visuales_actualizados.md',target)
    result=dict(files_updated=len(manifest),changed_prompts=len(changed),unchanged_prompts=84-len(changed),
                counts=counts(plan),backup=str(backup),major_assignments_preserved=9,genetic_reference_blocks_preserved=84)
    (STAGE/'verificacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    apply() if args.apply else stage()
