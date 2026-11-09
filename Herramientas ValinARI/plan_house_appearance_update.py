from pathlib import Path
import json
import random
import re
import secrets
import hashlib

WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IA\ValinARI\Valinari\Valinari')
POL=ROOT/'09_Politica'
PLAN=WORK/'cambios_apariencia_casas.json'
ORDER=WORK/'orden_visual_casas.json'

def main():
    backups=sorted((WORK/'respaldos_prompts').glob('*.md'))
    original=backups[0]
    names=[n.removeprefix('Casa ') for n in re.findall(r'^## (.+)$',original.read_text(encoding='utf-8-sig'),re.M)]
    assert len(names)==84 and len(set(names))==84
    ORDER.write_text(json.dumps(names,ensure_ascii=False,indent=2),encoding='utf-8')
    if PLAN.exists():
        print(PLAN.read_text(encoding='utf-8'))
        return
    images=list((ROOT/'07_Imagenes').rglob('*'))
    protected=[]
    candidates={}
    for folder in ['Casas Mayores','Casas Menores']:
        eligible=[]
        for p in sorted((POL/folder).glob('Casa *.md')):
            text=p.read_text(encoding='utf-8-sig')
            named_images=[str(im) for im in images if im.is_file() and (im.stem==p.stem or im.stem.startswith(p.stem+' '))]
            embedded=re.findall(r'!\[\[([^\]|]+)',text)
            if named_images or embedded:
                protected.append(dict(name=p.stem[5:],category=folder,path=str(p),images=named_images,embeds=embedded))
            else:
                eligible.append(p)
        candidates[folder]=eligible
    seed=secrets.randbits(64)
    rng=random.Random(seed)
    selected=[]
    for folder,hair,eyes in [('Casas Menores','castaño claro','verdes'),('Casas Mayores','pelirrojo','celestes')]:
        for p in rng.sample(candidates[folder],3):
            old=p.read_text(encoding='utf-8-sig')
            selected.append(dict(name=p.stem[5:],category=folder,path=str(p),hair=hair,eyes=eyes,
                                 original_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    plan=dict(random_seed=seed,old_order_source=str(original),protected=protected,selected=selected)
    PLAN.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(plan,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
