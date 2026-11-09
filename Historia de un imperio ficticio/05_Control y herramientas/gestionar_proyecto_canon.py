"""Project control driven by rutas_proyecto.json; default execution is read-only."""
from pathlib import Path
from datetime import datetime
import argparse, hashlib, json, os, csv

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def inspect(config):
    results = []
    for name, item in config['documents'].items():
        path = Path(item['path'])
        results.append({'documento': name, 'ruta': str(path), 'existe': path.is_file(),
                        'sha256': digest(path) if path.is_file() else None,
                        'funcion': item['role']})
    expected = config['provenance']
    actual = {r['documento']: r for r in results}
    checks = {
        'canon_coincide_con_revision_exportada': actual['canon']['sha256'] == expected['source_sha256'],
        'word_oficial_coincide_con_revision_exportada': actual['word']['sha256'] == expected['word_sha256'],
        'word_exportado_identico_al_oficial': actual['word_export']['sha256'] == actual['word']['sha256'],
        'pdf_coincide_con_render_verificado': actual['pdf_export']['sha256'] == expected['pdf_sha256'],
        'cronologia_coincide_con_registro': actual['chronology']['sha256'] == expected['chronology_sha256'],
    }
    return {'fecha': datetime.now().isoformat(timespec='seconds'), 'comprobaciones': checks,
            'actualizado': all(checks.values()) and all(r['existe'] for r in results), 'documentos': results,
            'nota': 'Esta comprobación verifica rutas y procedencia. No sustituye la auditoría de coherencia histórica ni la revisión visual.'}

def inventory(config, destination):
    fields = ['grupo', 'ruta', 'ruta_relativa', 'extension', 'bytes', 'modificado', 'relacion']
    errors=[]; count=0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('w', encoding='utf-8-sig', newline='') as stream:
        w=csv.DictWriter(stream, fieldnames=fields); w.writeheader()
        for name, value in config['inventory_roots'].items():
            root = Path(value)
            if not root.exists(): errors.append(str(root)); continue
            for folder, dirs, files in os.walk(root, followlinks=False):
                dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
                for filename in files:
                    p=Path(folder)/filename
                    if p == destination: continue
                    try:
                        st=p.stat()
                        w.writerow({'grupo':name,'ruta':str(p),'ruta_relativa':str(p.relative_to(root)),
                                    'extension':p.suffix.lower(),'bytes':st.st_size,
                                    'modificado':datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
                                    'relacion':'por clasificar' if name=='trabajo_local' else 'material del proyecto o de su proceso'})
                        count+=1
                    except OSError as e: errors.append(f'{p}: {e}')
    return {'archivo':str(destination),'archivos':count,'errores':errors}

def main():
    parser=argparse.ArgumentParser(description='Verificar originales, exportaciones y ubicaciones del proyecto Valinari')
    parser.add_argument('--config',type=Path,default=Path(__file__).with_name('rutas_proyecto.json'))
    parser.add_argument('--inventario',action='store_true',help='Actualizar solamente el catálogo de ubicaciones')
    parser.add_argument('--guardar-informe',action='store_true',help='Guardar el resultado de la verificación')
    args=parser.parse_args()
    config=json.loads(args.config.read_text(encoding='utf-8-sig'))
    result=inspect(config)
    if args.inventario:
        result['inventario']=inventory(config,Path(config['hub'])/'05_Control y herramientas/Inventario del proyecto.csv')
    if args.guardar_informe:
        out=Path(config['hub'])/'05_Control y herramientas/Estado de sincronizacion.json'
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['actualizado'] else 2)

if __name__=='__main__': main()
