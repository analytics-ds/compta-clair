#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Etape 1 de la banque d'images : chercher des candidats et generer la planche-contact.

Interroge Unsplash et Pexels sur les requetes de queries.yaml, ecarte les photos deja
presentes dans data/image-bank.yaml, puis ecrit :
  .image-bank-tmp/candidates.json       metadonnees de tous les candidats
  .image-bank-tmp/planche-contact.html  page locale de selection a ouvrir dans le navigateur

Aucune image n'est telechargee a cette etape : la planche affiche les vignettes distantes.
Le telechargement n'a lieu que pour les photos retenues, dans build-bank.py.

Usage :
    uv run .claude/scripts/image-bank/fetch-candidates.py [--per-source 6] [--category slug]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import yaml

from common import (
    CANDIDATES_FILE,
    QUERIES_FILE,
    SHEET_FILE,
    TMP_DIR,
    load_bank,
    load_env_keys,
    rel,
)

TIMEOUT = 25
# Pexels renvoie 403 sur le User-Agent par defaut d'urllib : on s'identifie explicitement.
USER_AGENT = "compta-clair-image-bank/1.0"


def http_json(url: str, headers: dict[str, str]) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **headers})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def search_unsplash(query: str, per_page: int, key: str) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape",
            "content_filter": "high",
        }
    )
    payload = http_json(
        f"https://api.unsplash.com/search/photos?{params}",
        {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"},
    )
    out = []
    for photo in payload.get("results", []):
        out.append(
            {
                "id": f"unsplash:{photo['id']}",
                "source": "unsplash",
                "thumb": photo["urls"]["small"],
                # `raw` accepte les parametres de redimensionnement d'Imgix.
                "full": photo["urls"]["raw"] + "&w=1600&q=85&fm=jpg",
                "page_url": photo["links"]["html"],
                # A appeler au moment ou la photo est reellement utilisee (ToS Unsplash).
                "download_location": photo["links"]["download_location"],
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"],
                "alt_en": (photo.get("alt_description") or "").strip(),
                "width": photo.get("width"),
                "height": photo.get("height"),
            }
        )
    return out


def search_pexels(query: str, per_page: int, key: str) -> list[dict]:
    params = urllib.parse.urlencode(
        {"query": query, "per_page": per_page, "orientation": "landscape", "size": "large"}
    )
    payload = http_json(
        f"https://api.pexels.com/v1/search?{params}", {"Authorization": key}
    )
    out = []
    for photo in payload.get("photos", []):
        out.append(
            {
                "id": f"pexels:{photo['id']}",
                "source": "pexels",
                "thumb": photo["src"]["medium"],
                "full": photo["src"]["large2x"],
                "page_url": photo["url"],
                "download_location": None,
                "author": photo["photographer"],
                "author_url": photo["photographer_url"],
                "alt_en": (photo.get("alt") or "").strip(),
                "width": photo.get("width"),
                "height": photo.get("height"),
            }
        )
    return out


def build_sheet(candidates: list[dict], groups: list[dict]) -> str:
    """Planche-contact autonome : vignettes cochables, selection persistee en localStorage."""
    payload = json.dumps(
        {"candidates": candidates, "groups": groups}, ensure_ascii=False, indent=None
    )
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Banque d'images — planche-contact</title>
<style>
  :root {
    --primary: #12433F; --primary-light: #E6F2EF; --accent: #9FE3D0;
    --text: #0D1D2F; --text-light: #5B6B7B; --border: #DDE5E3; --bg: #F9FAFB;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--text); background: var(--bg); padding: 24px 24px 96px;
  }
  h1 { font-size: 1.5rem; margin-bottom: 4px; }
  .intro { color: var(--text-light); font-size: 0.9rem; margin-bottom: 24px; max-width: 70ch; }
  h2 {
    font-size: 1rem; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--primary); margin: 32px 0 4px; padding-top: 16px;
    border-top: 1px solid var(--border);
  }
  .queries { color: var(--text-light); font-size: 0.8rem; margin-bottom: 12px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 12px; }
  .card {
    position: relative; border: 2px solid transparent; border-radius: 10px;
    overflow: hidden; background: #fff; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,.06);
  }
  .card.selected { border-color: var(--primary); box-shadow: 0 0 0 3px var(--accent); }
  .card img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; background: #eee; }
  .meta {
    display: flex; justify-content: space-between; gap: 8px;
    font-size: 0.72rem; color: var(--text-light); padding: 6px 8px;
  }
  .meta a { color: var(--text-light); }
  .badge {
    position: absolute; top: 8px; left: 8px; background: rgba(255,255,255,.92);
    border-radius: 999px; padding: 2px 8px; font-size: 0.68rem; font-weight: 600;
  }
  .tick {
    position: absolute; top: 8px; right: 8px; width: 24px; height: 24px; border-radius: 50%;
    background: rgba(255,255,255,.92); display: grid; place-items: center;
    font-size: 0.85rem; font-weight: 700; color: transparent;
  }
  .card.selected .tick { background: var(--primary); color: #fff; }
  .bar {
    position: fixed; bottom: 0; left: 0; right: 0; background: #fff;
    border-top: 1px solid var(--border); padding: 12px 24px;
    display: flex; align-items: center; gap: 16px; box-shadow: 0 -2px 8px rgba(0,0,0,.05);
  }
  .count { font-weight: 700; }
  button {
    font: inherit; font-weight: 600; font-size: 0.85rem; padding: 8px 16px;
    border-radius: 8px; border: 1px solid var(--primary); background: var(--primary);
    color: #fff; cursor: pointer;
  }
  button.ghost { background: #fff; color: var(--primary); }
  .hint { color: var(--text-light); font-size: 0.8rem; margin-left: auto; }
</style>
</head>
<body>
<h1>Banque d'images — planche-contact</h1>
<p class="intro">
  Clique sur les images a garder (vise 4 a 8 par categorie, en evitant deux photos trop
  proches). La selection est sauvegardee dans le navigateur : tu peux fermer et revenir.
  Quand c'est fini, telecharge la selection et lance build-bank.py.
</p>
<div id="sections"></div>
<div class="bar">
  <span class="count"><span id="n">0</span> image(s) selectionnee(s)</span>
  <button id="dl">Telecharger la selection</button>
  <button id="clear" class="ghost">Tout decocher</button>
  <span class="hint">puis : uv run .claude/scripts/image-bank/build-bank.py ~/Downloads/selection.json</span>
</div>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
(function () {
  var data = JSON.parse(document.getElementById('data').textContent);
  var KEY = 'image-bank-selection';
  var selected = new Set(JSON.parse(localStorage.getItem(KEY) || '[]'));
  var byCategory = {};
  data.candidates.forEach(function (c) {
    (byCategory[c.category] = byCategory[c.category] || []).push(c);
  });

  var host = document.getElementById('sections');
  data.groups.forEach(function (group) {
    var items = byCategory[group.category] || [];
    if (!items.length) return;
    var h2 = document.createElement('h2');
    h2.textContent = group.category + ' (' + items.length + ')';
    var queries = document.createElement('p');
    queries.className = 'queries';
    queries.textContent = group.queries.join(' · ');
    var grid = document.createElement('div');
    grid.className = 'grid';
    items.forEach(function (c) {
      var card = document.createElement('div');
      card.className = 'card' + (selected.has(c.id) ? ' selected' : '');
      card.innerHTML =
        '<img loading="lazy" src="' + c.thumb + '" alt="">' +
        '<span class="badge">' + c.source + '</span>' +
        '<span class="tick">&#10003;</span>' +
        '<span class="meta"><span>' + c.author + '</span></span>';
      card.addEventListener('click', function () {
        if (selected.has(c.id)) { selected.delete(c.id); card.classList.remove('selected'); }
        else { selected.add(c.id); card.classList.add('selected'); }
        save();
      });
      grid.appendChild(card);
    });
    host.append(h2, queries, grid);
  });

  function save() {
    localStorage.setItem(KEY, JSON.stringify([].concat(Array.from(selected))));
    document.getElementById('n').textContent = selected.size;
  }
  save();

  document.getElementById('dl').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(Array.from(selected), null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'selection.json';
    a.click();
    URL.revokeObjectURL(a.href);
  });

  document.getElementById('clear').addEventListener('click', function () {
    selected.clear();
    document.querySelectorAll('.card.selected').forEach(function (el) {
      el.classList.remove('selected');
    });
    save();
  });
})();
</script>
</body>
</html>
""".replace("__PAYLOAD__", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--per-source",
        type=int,
        default=6,
        help="nombre de candidats par requete et par source (defaut 6)",
    )
    parser.add_argument(
        "--category", help="ne traiter qu'une categorie (slug FR de queries.yaml)"
    )
    args = parser.parse_args()

    keys = load_env_keys()
    groups = yaml.safe_load(QUERIES_FILE.read_text(encoding="utf-8"))
    if args.category:
        groups = [g for g in groups if g["category"] == args.category]
        if not groups:
            raise SystemExit(f"Categorie inconnue dans {rel(QUERIES_FILE)} : {args.category}")

    known_ids = {entry["id"] for entry in load_bank()}
    candidates: list[dict] = []
    seen: set[str] = set()

    for group in groups:
        category = group["category"]
        for query in group["queries"]:
            for source, search, key in (
                ("unsplash", search_unsplash, keys["UNSPLASH_ACCESS_KEY"]),
                ("pexels", search_pexels, keys["PEXELS_API_KEY"]),
            ):
                try:
                    results = search(query, args.per_source, key)
                except urllib.error.HTTPError as error:
                    print(
                        f"  ! {source} {query!r} : HTTP {error.code} ({error.reason})",
                        file=sys.stderr,
                    )
                    continue
                except urllib.error.URLError as error:
                    print(f"  ! {source} {query!r} : {error.reason}", file=sys.stderr)
                    continue
                kept = 0
                for candidate in results:
                    if candidate["id"] in known_ids or candidate["id"] in seen:
                        continue
                    seen.add(candidate["id"])
                    candidate["category"] = category
                    candidate["query"] = query
                    candidate["tags"] = group.get("tags", [])
                    candidates.append(candidate)
                    kept += 1
                print(f"  {category} · {source} · {query!r} : {kept} candidat(s)")

    if not candidates:
        raise SystemExit("Aucun candidat — toutes les photos sont deja dans la banque ?")

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATES_FILE.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    SHEET_FILE.write_text(build_sheet(candidates, groups), encoding="utf-8")

    print(f"\n{len(candidates)} candidats ecrits dans {rel(CANDIDATES_FILE)}")
    print(f"Planche-contact : {SHEET_FILE}")
    print(f"  open '{SHEET_FILE}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
