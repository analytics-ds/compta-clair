#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Etape 2 de la banque d'images : telecharger la selection et remplir l'index.

Prend le selection.json exporte par la planche-contact, telecharge chaque photo retenue
en pleine resolution, la recadre en 1200x675, la convertit en WebP dans
static/images/banque/, et ajoute son entree dans data/image-bank.yaml.

Les alt_fr / alt_en sont laisses vides : c'est Claude qui les redige ensuite, une image
sans alt_fr n'est pas tirable par /create-article-geo.

Usage :
    uv run .claude/scripts/image-bank/build-bank.py ~/Downloads/selection.json
    uv run .claude/scripts/image-bank/build-bank.py mark-used <fichier.webp> <slug-article>
    uv run .claude/scripts/image-bank/build-bank.py stats
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from common import (
    IMAGES_DIR,
    load_bank,
    load_candidates,
    load_env_keys,
    rel,
    save_bank,
)

TARGET_W, TARGET_H = 1200, 675
WEBP_QUALITY = "82"
TIMEOUT = 60
USER_AGENT = "les-cles-du-dirigeant-image-bank/1.0"

SOURCE_LABEL = {"unsplash": "Unsplash", "pexels": "Pexels"}


def run(*command: str) -> None:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{command[0]} a echoue : {result.stderr.strip()}")


def pixel_size(path: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    width = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    height = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return width, height


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        destination.write_bytes(response.read())


def to_webp(source: Path, destination: Path) -> None:
    """Recadre en 1200x675 (centre) puis convertit en WebP.

    On redimensionne d'abord sur le cote qui manque de pixels, sinon `sips -c` completerait
    l'image avec du blanc au lieu de la rogner.
    """
    width, height = pixel_size(source)
    if width / height >= TARGET_W / TARGET_H:
        run("sips", "--resampleHeight", str(TARGET_H), str(source))
    else:
        run("sips", "--resampleWidth", str(TARGET_W), str(source))
    run("sips", "-c", str(TARGET_H), str(TARGET_W), str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    run("cwebp", "-quiet", "-q", WEBP_QUALITY, str(source), "-o", str(destination))


def ping_unsplash_download(candidate: dict, key: str) -> None:
    """Declenche l'endpoint de download Unsplash, requis par leurs conditions d'API."""
    location = candidate.get("download_location")
    if not location:
        return
    separator = "&" if "?" in location else "?"
    request = urllib.request.Request(
        f"{location}{separator}client_id={key}", headers={"Accept-Version": "v1"}
    )
    try:
        urllib.request.urlopen(request, timeout=TIMEOUT).read()
    except urllib.error.URLError as error:
        print(f"  ! ping download Unsplash echoue : {error}", file=sys.stderr)


def clean_author(name: str) -> str:
    """Certains contributeurs Pexels ont une URL en guise de nom : on garde le domaine."""
    name = (name or "").strip()
    if name.startswith(("http://", "https://")):
        return name.split("//", 1)[1].strip("/").removeprefix("www.")
    return name or "auteur inconnu"


def next_filename(category: str, taken: set[str]) -> str:
    index = 1
    while f"{category}-{index:02d}.webp" in taken:
        index += 1
    return f"{category}-{index:02d}.webp"


def cmd_build(selection_path: Path) -> int:
    if not selection_path.is_file():
        raise SystemExit(f"Selection introuvable : {selection_path}")
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    candidates = {c["id"]: c for c in load_candidates()}
    bank = load_bank()
    known = {entry["id"] for entry in bank}
    taken = {entry["file"] for entry in bank}
    keys = load_env_keys()

    added = 0
    for image_id in selection:
        if image_id in known:
            print(f"  = {image_id} deja dans la banque")
            continue
        candidate = candidates.get(image_id)
        if not candidate:
            print(f"  ! {image_id} absent de candidates.json — ignore", file=sys.stderr)
            continue

        filename = next_filename(candidate["category"], taken)
        destination = IMAGES_DIR / filename
        try:
            with tempfile.TemporaryDirectory() as tmp:
                raw = Path(tmp) / "source.jpg"
                download(candidate["full"], raw)
                to_webp(raw, destination)
        except (urllib.error.URLError, RuntimeError) as error:
            print(f"  ! {image_id} : {error}", file=sys.stderr)
            continue

        if candidate["source"] == "unsplash":
            ping_unsplash_download(candidate, keys["UNSPLASH_ACCESS_KEY"])

        taken.add(filename)
        known.add(image_id)
        bank.append(
            {
                "id": image_id,
                "file": filename,
                "path": f"/images/banque/{filename}",
                "categories": [candidate["category"]],
                "tags": list(candidate.get("tags", [])),
                "alt_fr": "",
                "alt_en": "",
                "alt_source_en": candidate.get("alt_en", ""),
                "credit": (
                    f"Photo de {clean_author(candidate['author'])} sur "
                    f"{SOURCE_LABEL.get(candidate['source'], candidate['source'])}"
                ),
                "source_url": candidate["page_url"],
                "added": date.today().isoformat(),
                "used_by": [],
            }
        )
        added += 1
        print(f"  + {filename}  ({candidate['source']} · {candidate['author']})")

    save_bank(bank)
    print(f"\n{added} image(s) ajoutee(s). Banque : {len(bank)} image(s).")
    missing_alt = [e["file"] for e in bank if not e["alt_fr"]]
    if missing_alt:
        print(f"{len(missing_alt)} image(s) sans alt_fr — a rediger avant tirage.")
    return 0


def cmd_mark_used(image: str, slug: str) -> int:
    bank = load_bank()
    for entry in bank:
        if image in (entry["file"], entry["id"], entry["path"]):
            if slug not in entry["used_by"]:
                entry["used_by"].append(slug)
            save_bank(bank)
            print(f"{entry['file']} -> used_by: {entry['used_by']}")
            return 0
    raise SystemExit(f"Image introuvable dans la banque : {image}")


def cmd_stats() -> int:
    bank = load_bank()
    if not bank:
        print("Banque vide.")
        return 0
    by_category: dict[str, list[dict]] = {}
    for entry in bank:
        for category in entry["categories"]:
            by_category.setdefault(category, []).append(entry)
    print(f"{len(bank)} image(s) dans {rel(IMAGES_DIR)}\n")
    print(f"{'categorie':<32} {'total':>6} {'libres':>7} {'sans alt':>9}")
    for category, entries in sorted(by_category.items()):
        free = sum(1 for e in entries if not e["used_by"])
        no_alt = sum(1 for e in entries if not e["alt_fr"])
        print(f"{category:<32} {len(entries):>6} {free:>7} {no_alt:>9}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    build = sub.add_parser("build", help="ajouter la selection a la banque (defaut)")
    build.add_argument("selection", type=Path)

    used = sub.add_parser("mark-used", help="noter qu'un article utilise une image")
    used.add_argument("image", help="nom de fichier, chemin Hugo ou id de l'image")
    used.add_argument("slug", help="slug de l'article")

    sub.add_parser("stats", help="etat de la banque par categorie")

    # `build-bank.py <selection.json>` sans sous-commande = build
    argv = sys.argv[1:]
    if argv and argv[0] not in {"build", "mark-used", "stats", "-h", "--help"}:
        argv = ["build", *argv]
    args = parser.parse_args(argv)

    if args.command == "mark-used":
        return cmd_mark_used(args.image, args.slug)
    if args.command == "stats":
        return cmd_stats()
    if args.command == "build":
        return cmd_build(args.selection)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
