"""Utilitaires partages par les scripts de la banque d'images.

Chemins, lecture des cles API et lecture/ecriture de data/image-bank.yaml.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

# .claude/scripts/image-bank/common.py -> racine du site Hugo
ROOT = Path(__file__).resolve().parents[3]

QUERIES_FILE = ROOT / ".claude/scripts/image-bank/queries.yaml"
BANK_FILE = ROOT / "data/image-bank.yaml"
IMAGES_DIR = ROOT / "static/images/banque"
TMP_DIR = ROOT / ".image-bank-tmp"
CANDIDATES_FILE = TMP_DIR / "candidates.json"
SHEET_FILE = TMP_DIR / "planche-contact.html"

BANK_HEADER = """\
# Banque d'images de Compta Clair — index lu par Claude (/create-article-geo) et par Hugo.
#
# Genere par .claude/scripts/image-bank/build-bank.py, a partir d'une selection validee
# a la main sur la planche-contact. Ne pas ajouter d'entree a la main sans copier le
# fichier image correspondant dans static/images/banque/.
#
# Champs :
#   id         source:identifiant, sert a ne jamais re-telecharger deux fois la meme photo
#   file/path  nom du fichier WebP et chemin Hugo
#   categories slugs FR de data/categories.yaml — premier filtre du tirage
#   tags       mots-cles FR — second filtre, matches avec le sujet de l'article
#   alt_fr     texte alternatif francais (max 125 car.), a ecrire par Claude
#   alt_en     texte alternatif anglais (max 125 car.), a ecrire par Claude
#   credit     mention affichee sous l'image de l'article (obligatoire)
#   used_by    slugs des articles qui utilisent deja cette image (evite les doublons)
#
# `alt_fr: ""` signifie que l'image n'est pas encore utilisable : Claude doit rediger
# les deux alt avant le premier tirage.
"""


def load_env_keys() -> dict[str, str]:
    """Cles API depuis <drive>/.claude/secrets/.env (convention CLAUDE.md de l'equipe).

    Le fichier de secrets vit a la racine du Drive partage, plusieurs niveaux au-dessus
    du site : on remonte l'arborescence jusqu'a le trouver. Les valeurs ne sont jamais
    ecrites ailleurs que dans la memoire du process.
    """
    for parent in [ROOT, *ROOT.parents]:
        env_path = parent / ".claude/secrets/.env"
        if env_path.is_file():
            keys = {}
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, value = line.partition("=")
                keys[name.strip()] = value.strip().strip('"').strip("'")
            missing = [
                k for k in ("UNSPLASH_ACCESS_KEY", "PEXELS_API_KEY") if not keys.get(k)
            ]
            if missing:
                raise SystemExit(
                    f"Cles manquantes dans {env_path} : {', '.join(missing)}"
                )
            return keys
    raise SystemExit(
        "Fichier .claude/secrets/.env introuvable en remontant depuis " + str(ROOT)
    )


def load_bank() -> list[dict]:
    if not BANK_FILE.is_file():
        return []
    data = yaml.safe_load(BANK_FILE.read_text(encoding="utf-8"))
    return data or []


def save_bank(entries: list[dict]) -> None:
    BANK_FILE.parent.mkdir(parents=True, exist_ok=True)
    body = yaml.safe_dump(
        entries, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100
    )
    BANK_FILE.write_text(BANK_HEADER + "\n" + body, encoding="utf-8")


def load_candidates() -> list[dict]:
    if not CANDIDATES_FILE.is_file():
        raise SystemExit(
            f"{CANDIDATES_FILE} introuvable — lancer d'abord fetch-candidates.py"
        )
    return json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    """Chemin lisible, relatif a la racine du site quand c'est possible."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)

