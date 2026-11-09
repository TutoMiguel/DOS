from pathlib import Path
import re

ROOT = Path(r"C:\IA\ValinARI\Valinari\Valinari\09_Politica")

def split_sections(text):
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.M))
    sections = {}
    for i, m in enumerate(matches):
        key = m.group(1).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[key] = text[m.end():end].strip()
    return sections

def get_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[:end + 4].strip()
    return ""

def body_without_sections(text):
    fm = get_frontmatter(text)
    return text[len(fm):].strip() if fm else text.strip()

def title(text):
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    return m.group(1).strip() if m else "Casa"

def normalize(path, category):
    text = path.read_text(encoding="utf-8")
    fm = get_frontmatter(text)
    sections = split_sections(body_without_sections(text))
    t = title(body_without_sections(text))
    # Normalize legacy names without discarding their contents.
    aliases = {
        "Origen geográfico fundacional": "Origen geográfico",
        "Carta heráldica revisada": "Carta heráldica y visual",
        "Fenotipo cortesano canónico": "Perfil fenotípico cortesano",
    }
    for old, new in aliases.items():
        if old in sections and new not in sections:
            sections[new] = sections.pop(old)

    if category == "major":
        regime = "Casa Mayor con asiento y voto en el Consejo de las 24 Casas. Conserva patrimonio, jurisdicción interna y representación histórica dentro de la monarquía pactada."
    elif category == "minor":
        regime = "Casa Menor de Exploración y Comercio. No posee asiento propio en el Consejo; ejerce autoridad mediante funciones comerciales, marítimas, cartográficas o de asentamiento."
    elif category == "vassal":
        regime = "Casa Vasalla subordinada a una Casa Mayor tutelar. Conserva patrimonio y representación local, pero no posee voto independiente en el Consejo."
    else:
        regime = "Casa Real de Valinor. Ejerce la Corona conforme a los pactos históricos, al Consejo de las 24 Casas y a las instituciones constitucionales vigentes."

    if "Régimen político" not in sections:
        sections["Régimen político"] = regime
    if category == "vassal" and "Casa tutelar" not in sections:
        status = re.search(r"Casa (?:Vasalla de|Menor de|noble|Real).*", text)
        sections["Casa tutelar"] = "La casa queda vinculada a la Casa Mayor indicada en su estatus y en su índice político."
    if "Personajes asociados" not in sections:
        sections["Personajes asociados"] = "No hay personajes individualizados en esta ficha. Se añadirán cuando el canon los reconozca."
    if "Carta heráldica y visual" not in sections:
        sections["Carta heráldica y visual"] = "La representación visual debe conservar el blasón y el estandarte descritos en esta ficha, respetando el sindarin, el alto tengwar y la paleta heráldica canónica."
    if "Referencias genéticas orientativas" not in sections:
        sections["Referencias genéticas orientativas"] = "- HERC2/OCA2: pigmentación del iris.\n- KITLG, IRF4, SLC24A4, TYRP1 y TPCN2: pigmentación capilar.\n- SLC24A5, SLC45A2, TYR y OCA2: melanogénesis y piel.\n- MC1R: pecas y variación de pigmentación.\n- EDAR, TCHH, KRT71 y FGFR2: forma del cabello.\n\nEstas referencias son orientativas y poligénicas; no constituyen genotipos obligatorios ni rasgos exclusivos."
    if category == "vassal" and "Genotipo poblacional orientativo" in sections:
        # Keep the requested detail, but place it with the phenotype material.
        pass
    if "Matriz funcional y heráldica" not in sections:
        sections["Matriz funcional y heráldica"] = "[[../Matriz Heráldica y Funcional de las Casas]]"

    order = [
        "Estatus", "Casa tutelar", "Origen geográfico", "Característica histórica",
        "Función histórica", "Relación política", "Régimen político", "Blasón",
        "Estandarte", "Lema", "Carta heráldica y visual", "Miembros conocidos en 833 d.C.",
        "Personajes asociados", "Perfil fenotípico canónico", "Perfil fenotípico cortesano",
        "Genotipo poblacional orientativo", "Referencias genéticas orientativas",
        "Relaciones", "Enlaces de gestión", "Referencias relacionadas",
        "Matriz funcional y heráldica"
    ]
    # Capture title-level status lines into the Estatus section when absent.
    if "Estatus" not in sections:
        m = re.search(r"\*\*Estatus:\*\*\s*(.+)", text)
        sections["Estatus"] = m.group(1).strip() if m else "Casa noble."
    out = [fm, f"# {t}"] if fm else [f"# {t}"]
    for key in order:
        if key in sections:
            content = sections[key].strip()
            out += ["", f"## {key}", "", content]
    path.write_text("\n".join(out).strip() + "\n", encoding="utf-8")

def run(folder, category):
    for p in sorted(folder.glob("Casa *.md")):
        normalize(p, category)

run(ROOT / "Casas Mayores", "major")
run(ROOT / "Casas Menores", "minor")
run(ROOT / "Casas Vasallas", "vassal")
run(ROOT / "Casa Real", "royal")
