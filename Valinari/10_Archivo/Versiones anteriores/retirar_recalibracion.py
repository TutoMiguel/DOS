from pathlib import Path
import re

p = Path('actualizaciones_acumulativas_canon_v12.md')
s = p.read_text(encoding='utf-8')
# Retira las secciones completas de economía/recalibración anteriores (14 y 15).
s = re.sub(r'\n## 14\. Actualización acumulativa — economía del Reino y de la Federación.*?(?=\n## 16\. Ficha geográfica canónica — Valinor a Tyl)', '\n', s, flags=re.S)
s = re.sub(r'\n## 15\. Recalibración demográfica territorial — Arnor y Calenardhon Austral.*?(?=\n## 16\. Ficha geográfica canónica — Valinor a Tyl)', '\n', s, flags=re.S)
p.write_text(s, encoding='utf-8')
print('recalibracion retirada')
