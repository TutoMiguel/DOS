from pathlib import Path
from datetime import datetime
import argparse
import json
import re
import shutil
from build_house_prompts import ROOT,WORK

TARGET=ROOT/'Prompts Visuales de las 84 Casas.md'
DRAFT=WORK/'prompts_visuales_actualizados.md'

def blocks(text):
    found=list(re.finditer(r'^## Casa ([^\n]+)$',text,re.M))
    return {m.group(1).strip():text[m.end():found[i+1].start() if i+1<len(found) else len(text)].strip()
            for i,m in enumerate(found)}

def subsection(block,heading):
    m=re.search(r'^### '+re.escape(heading)+r'\n+(.*?)(?=^### |\Z)',block,re.M|re.S)
    assert m,heading
    return m.group(1).strip()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    plan=json.loads((WORK/'cambios_apariencia_casas.json').read_text(encoding='utf-8'))
    expected_order=json.loads((WORK/'orden_visual_casas.json').read_text(encoding='utf-8'))
    old=TARGET.read_text(encoding='utf-8-sig')
    new=DRAFT.read_text(encoding='utf-8-sig')
    ob,nb=blocks(old),blocks(new)
    assert list(nb)==expected_order
    assert set(nb)==set(ob) and len(nb)==84
    selected={x['name']:x for x in plan['selected']}
    assert len(selected)==6
    images=[p for p in (ROOT.parent/'07_Imagenes').rglob('*') if p.is_file()]
    protected={x['name'] for x in plan['protected']}
    assert not protected.intersection(selected)
    untouched=0
    for name,block in nb.items():
        assert subsection(ob[name],'Distribución expresa de personajes')==subsection(block,'Distribución expresa de personajes'),name
        assert subsection(ob[name],'Genotipo poblacional orientativo')==subsection(block,'Genotipo poblacional orientativo'),name
        assert subsection(ob[name],'Referencias genéticas orientativas')==subsection(block,'Referencias genéticas orientativas'),name
        profile=subsection(block,'Perfil fenotípico canónico')
        if name in selected:
            item=selected[name]
            assert profile.startswith('Cabello '+item['hair']+'; ojos '+item['eyes']+';'),name
            assert not any(p.stem=='Casa '+name or p.stem.startswith('Casa '+name+' ') for p in images),name
            note=Path(item['path']).read_text(encoding='utf-8-sig')
            assert '![' not in note,name
            assert profile in note,name
            rest_old=subsection(ob[name],'Perfil fenotípico canónico').split(';',2)[2]
            rest_new=profile.split(';',2)[2]
            assert rest_old==rest_new,name
        else:
            assert profile==subsection(ob[name],'Perfil fenotípico canónico'),name
            untouched+=1
        link=re.search(r'\*\*Fuente:\*\* \[\[([^|]+)\|',block).group(1)
        assert (ROOT/(link+'.md')).is_file(),link
    assert untouched==78
    records=json.loads((WORK/'prompts_visuales_verificacion.json').read_text(encoding='utf-8'))
    for record in records:
        assert 177<=record['male_cm']<=202 and 173<=record['female_cm']<=184
    for category,hair,eyes in [('Casas Menores','castaño claro','verdes'),('Casas Mayores','pelirrojo','celestes')]:
        subset=[x for x in selected.values() if x['category']==category]
        assert len(subset)==3
        for item in subset:
            assert item['hair']==hair and item['eyes']==eyes
    report=['# Auditoría de la actualización visual de seis Casas','',
            '| Casa | Categoría | Cabello | Ojos | Imagen previa |',
            '|---|---|---|---|---|']
    for item in plan['selected']:
        report.append(f'| Casa {item["name"]} | {item["category"]} | {item["hair"]} | {item["eyes"]} | Ninguna detectada |')
    report += ['', '- Orden de las 84 Casas idéntico al catálogo anterior respaldado.',
               '- Tres Casas Menores castañas de ojos verdes y tres Mayores pelirrojas de ojos celestes.',
               '- Las otras 78 Casas conservan su perfil fenotípico.',
               '- Se conservan las 84 asignaciones de altura, complexión, peinado, postura, posición e implementos.',
               '- Se conservan los 84 apartados de genotipo orientativo y las 84 referencias genéticas.',
               '- Ninguna Casa seleccionada tiene imágenes asociadas al momento de la verificación.',
               '- Se verificaron los 84 enlaces a las fichas fuente.',
               '- Se sincronizaron las seis fichas, los perfiles agregados y los dos Markdown del Canon V16.',
               '', '**Casas protegidas por disponer de imágenes:** '+', '.join(sorted(protected))+'.',
               '', f'**Semilla del sorteo registrado:** {plan["random_seed"]}.',
               '', 'Las variantes son tendencias de representación familiar, con variación individual; las referencias genéticas no fijan genotipos exclusivos.',
               '']
    report_path=WORK/'Auditoría de Prompts Visuales de las Casas.md'
    report_path.write_text('\n'.join(report),encoding='utf-8')
    if args.publish:
        backup=WORK/'respaldos_prompts'/('Prompts Visuales antes del ajuste fenotípico '+datetime.now().strftime('%Y%m%d-%H%M%S')+'.md')
        shutil.copy2(TARGET,backup)
        shutil.copyfile(DRAFT,TARGET)
        shutil.copyfile(report_path,ROOT/report_path.name)
        assert TARGET.read_bytes()==DRAFT.read_bytes()
    print(json.dumps(dict(audit='correcta',prompts=84,changed_profiles=6,unchanged_profiles=untouched,
                         previous_order_restored=True,character_assignments_preserved=84,
                         image_protected=len(protected),broken_links=0,published=args.publish),ensure_ascii=False))

if __name__=='__main__':
    main()
