"""Stage and publish a recorded random hair allocation for nine unillustrated houses."""
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
from build_house_prompts import ROOT, WORK, sections

VAULT = ROOT.parent
STAGE = WORK / 'redistribucion_capilar_nueve_casas'
PLAN = STAGE / 'sorteo.json'
MANIFEST = STAGE / 'manifest.json'
NAMES = ['Harlond', 'Harnost', 'Minas Anor', 'Mithlond', 'Pelargir',
         'Rhunost', 'Taur-en-Mor', 'Teleri', 'Vanyar']
TITLE = 'Distribución capilar de las nueve Casas Mayores pendientes'
PALETTE = ['rubio ceniza', 'pelirrojo', 'rubio muy claro', 'pelirrojo',
           'rubio dorado', 'rubio oscuro', 'rubio ceniza', 'rubio claro', 'rubio platino']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return path.read_text(encoding='utf-8-sig')

def illustrated():
    out = {}
    for p in sorted((ROOT/'Casas Mayores').glob('Casa *.md')):
        refs = re.findall(r'!\[\[([^\]|]+)', read(p))
        good = [x for x in refs if (VAULT/'07_Imagenes'/x).is_file()]
        if good:
            out[p.stem[5:]] = good
    return out

def draw():
    existing = illustrated()
    all_names = {p.stem[5:] for p in (ROOT/'Casas Mayores').glob('Casa *.md')}
    assert len(all_names) == 24 and all_names-set(existing) == set(NAMES)
    assert all('![[ ' not in read(ROOT/'Casas Mayores'/f'Casa {n}.md') for n in NAMES)
    if PLAN.exists():
        plan = json.loads(read(PLAN))
    else:
        seed = random.SystemRandom().getrandbits(64)
        rng = random.Random(seed)
        male, female = PALETTE.copy(), PALETTE.copy()
        rng.shuffle(male)
        rng.shuffle(female)
        plan = dict(seed=str(seed), algorithm='Dos permutaciones independientes de la misma paleta, una por sexo; sin resorteo.',
                    scope='Nueve Casas Mayores pendientes, dieciocho representantes adultos anónimos.',
                    illustrated_protected=existing,
                    allocation=[dict(name=n,male=m,female=f) for n,m,f in zip(NAMES,male,female)])
        PLAN.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    for sex in ('male','female'):
        assert sum(x[sex]=='pelirrojo' for x in plan['allocation']) == 2
        assert Counter(x[sex] for x in plan['allocation']) == Counter(PALETTE)
    assert len({x['name'] for x in plan['allocation']}) == 9
    return plan

def stage():
    STAGE.mkdir(exist_ok=True)
    plan = draw()
    changes = {}
    allocations = plan['allocation']
    table = ['| Casa | Cabello del hombre | Cabello de la mujer |', '|---|---|---|']
    for x in allocations:
        table.append(f'| [[Casas Mayores/Casa {x["name"]}|Casa {x["name"]}]] | {x["male"]} | {x["female"]} |')
        p = ROOT/'Casas Mayores'/f'Casa {x["name"]}.md'
        old = read(p)
        block = ('## Representantes de la galería\n\n'
                 'Pareja adulta anónima para la imagen individual de esta Casa.\n\n'
                 f'- **Cabello del hombre:** {x["male"]}\n'
                 f'- **Cabello de la mujer:** {x["female"]}\n\n'
                 'El color se asigna individualmente a cada cónyuge. El perfil familiar describe tendencias '
                 'con variación interna; los matrimonios entre linajes permiten parejas de distinto color '
                 'natural de cabello. Se conservan los ojos, piel, pecas y textura capilar de la ficha, '
                 'así como las alturas, complexiones, peinados, posturas e implementos ya fijados.\n\n'
                 f'[[../{TITLE}|Distribución de las nueve parejas pendientes]].\n\n')
        if '## Representantes de la galería' in old:
            new = re.sub(r'(?ms)^## Representantes de la galería\n.*?(?=^## |\Z)',lambda _:block,old,count=1)
        else:
            assert '## Personajes asociados' in old
            new = old.replace('## Personajes asociados',block+'## Personajes asociados',1)
        before, after = sections(old), sections(new)
        for heading in ('Perfil fenotípico canónico','Genotipo poblacional orientativo','Referencias genéticas orientativas'):
            assert before.get(heading) == after.get(heading), (x['name'],heading)
        changes[p] = new
    lines = ['---','tipo: distribución visual','canon: V16','casas: 9','representantes: 18','---',
             '# '+TITLE,'',
             'Sorteo adoptado por el autor para las nueve parejas todavía sin imagen: siete hombres y siete '
             'mujeres con tonos rubios habituales, dos hombres y dos mujeres de cabello pelirrojo. '
             'Los colores masculinos y femeninos se permutan por separado.','',*table,'',
             'Esta asignación corresponde a individuos de la galería; las tendencias familiares admiten variación '
             'y matrimonios entre linajes. El color de ojos y los demás rasgos conservan su referencia en cada ficha.','',
             'Se mantienen las alturas, posiciones, posturas, cortes, barbas, texturas, objetos de oficio y heráldica. '
             'La pareja pelirroja ya ilustrada de Casa Fornost se conserva.','',
             f'Casas Mayores: 24 en total, {len(plan["illustrated_protected"])} con imagen asignada y 9 pendientes.','',
             '## Registro del sorteo','',f'Semilla: {plan["seed"]}. {plan["algorithm"]}','',
             '## Referencias relacionadas','',
             '- [[Prompts Visuales de las 84 Casas]]',
             '- [[Perfil Fenotípico/Casas Mayores|Perfiles familiares de las Casas Mayores]]',
             '- [[Casas Mayores/Índice de Casas Mayores]]','']
    changes[ROOT/(TITLE+'.md')] = '\n'.join(lines)
    summary = ('Las nueve parejas de la galería pendientes de imagen tienen una asignación capilar individual '
               'registrada por separado para cada cónyuge. En conjunto, siete hombres y siete mujeres '
               'conservan tonos rubios habituales; dos hombres y dos mujeres son pelirrojos. '
               'El reparto admite matrimonios de distinto color natural de cabello, dentro de la variación '
               'humana de los linajes. Esta asignación individual prevalece sobre la tendencia capilar '
               'general de la Casa al representar a estos dieciocho personajes.')
    plain_table = '\n'.join(table)
    for p in (WORK/'Canon V16 Maestro.md',VAULT/'00_Canon'/'Canon V16 Maestro.md'):
        text = read(p)
        text = text.replace('Las Casas Mayores Fornost, Harnost, Mithlond se representan con cabello pelirrojo y ojos celestes.',
                            'Los perfiles familiares de Fornost, Harnost y Mithlond registran cabello pelirrojo y ojos celestes; '
                            'las parejas de la galería admiten la variación individual expresamente asignada a cada cónyuge.')
        block = '\n\n### Distribución individual de las nueve parejas pendientes\n\n'+summary+'\n\n'+plain_table+'\n'
        # Canon links must resolve relative to their own locations, not the political folder.
        block = block.replace('[[Casas Mayores/', '[[09_Politica/Casas Mayores/')
        if '### Distribución individual de las nueve parejas pendientes' not in text:
            text += block
        changes[p] = text
    for p in (ROOT/'Perfil Fenotípico'/'Casas Mayores.md',ROOT/'Perfil Fenotípico'/'Perfil Fenotípico del reino.md'):
        text=read(p)
        note = '\n\n## Colores individuales de la galería\n\n'+summary+'\n\n'+f'[[../{TITLE}|Reparto individual de las nueve parejas]].\n'
        if '## Colores individuales de la galería' not in text:
            text+=note
        changes[p]=text
    p=VAULT/'00_Canon'/'Registro de Cambios.md'
    changes[p]=read(p)+'\n- Reparto capilar individual adoptado para nueve parejas pendientes: siete hombres y siete mujeres rubios, '
    changes[p]+='dos hombres y dos mujeres pelirrojos; sorteo independiente por sexo, con matrimonios de distinto color. '
    changes[p]+='Se conserva la pareja ilustrada de Fornost. Semilla registrada en la ficha de distribución visual.\n'
    p=ROOT/'Auditoría de Prompts Visuales de las Casas.md'
    text=read(p)
    if not text.startswith('> Antecedente'):
        text='> Antecedente del primer sorteo. El reparto individual vigente de las nueve parejas pendientes se documenta al final.\n\n'+text
    text+='\n\n## Reparto individual vigente de las nueve parejas pendientes\n\n'+summary+'\n\n'+plain_table+'\n'
    text+='\nLas quince Casas Mayores ya ilustradas conservan sus asignaciones. Se mantienen los 84 genotipos y referencias genéticas del catálogo.\n'
    changes[p]=text
    manifest=[]
    for i,(p,text) in enumerate(changes.items()):
        dest=STAGE/f'{i:02d}.md'
        dest.write_text(text,encoding='utf-8')
        manifest.append(dict(target=str(p),stage=str(dest),before=digest(p.read_bytes()) if p.exists() else None,
                             after=digest(dest.read_bytes())))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(staged=len(manifest),allocation=allocations,seed=plan['seed']),ensure_ascii=False))

def apply():
    plan=json.loads(read(PLAN))
    assert set(illustrated())==set(plan['illustrated_protected'])
    manifest=json.loads(read(MANIFEST))
    for x in manifest:
        p=Path(x['target'])
        assert (digest(p.read_bytes()) if p.exists() else None)==x['before'],p
    backup=STAGE/('respaldo-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    backup.mkdir()
    for i,x in enumerate(manifest):
        p=Path(x['target'])
        if p.exists(): shutil.copy2(p,backup/f'{i:02d}-{p.name}')
        shutil.copy2(x['stage'],p)
    assignments=WORK/'asignaciones_visuales_casas.json'
    shutil.copy2(assignments,backup/assignments.name)
    old_records=json.loads(read(assignments))
    target=ROOT/'Prompts Visuales de las 84 Casas.md'
    old_catalog=read(target)
    shutil.copy2(target,backup/target.name)
    subprocess.run([sys.executable,str(WORK/'build_house_prompts.py')],check=True,cwd=WORK)
    new_catalog=read(WORK/'prompts_visuales_actualizados.md')
    old_chunks={m.group(1):m.group(0).strip() for m in re.finditer(r'(?ms)^## Casa (.+?)\n.*?(?=^## Casa |^# Casa |\Z)',old_catalog)}
    new_chunks={m.group(1):m.group(0).strip() for m in re.finditer(r'(?ms)^## Casa (.+?)\n.*?(?=^## Casa |^# Casa |\Z)',new_catalog)}
    assert list(old_chunks)==list(new_chunks) and len(new_chunks)==84
    changed={n for n in old_chunks if old_chunks[n]!=new_chunks[n]}
    assert changed==set(NAMES),changed
    new_records=json.loads(read(assignments))
    keys=('name','male_cm','female_cm','male_side','female_side','male_pose','female_pose','female_item','male_item','armed','role','visual_index')
    for before,after in zip(old_records,new_records):
        assert all(before[k]==after[k] for k in keys),before['name']
    for sex in ('male','female'):
        assert sum(r.get(sex+'_hair_color')=='pelirrojo' for r in new_records)==2
    for x in plan['allocation']:
        r=next(r for r in new_records if r['name']==x['name'])
        assert r['male_hair_color']==x['male'] and r['female_hair_color']==x['female']
    shutil.copy2(WORK/'prompts_visuales_actualizados.md',target)
    report=dict(major_houses=24,illustrated=15,pending=9,changed_prompt_blocks=9,
                unchanged_prompt_blocks=75,male_redheads=2,female_redheads=2,male_common=7,female_common=7,
                mixed_hair_couples=sum(x['male']!=x['female'] for x in plan['allocation']),
                allocation=plan['allocation'],backup=str(backup),seed=plan['seed'])
    (STAGE/'verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    apply() if args.apply else stage()
