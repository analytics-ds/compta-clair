#!/bin/bash
# deploy-pages.sh
# Publie le site sur GitHub Pages : https://analytics-ds.github.io/compta-clair/
#
# Deploiement manuel de SECOURS. En temps normal le site est construit et publie par
# .github/workflows/hugo.yml a chaque push sur main ; ce script ne sert que si Actions est
# indisponible. Il pousse le site deja construit dans le clone `.deploy/`.
#
# Chaine : build Hugo -> synchro dans .deploy/ -> controle de fuite -> commit -> push.
#
# Usage : bash .claude/scripts/deploy-pages.sh ["message de commit"]

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEPLOY="$ROOT/.deploy"
MESSAGE="${1:-Met a jour le site}"

cd "$ROOT"

if [ ! -d "$DEPLOY/.git" ]; then
    echo "ERREUR : $DEPLOY n'est pas un clone de analytics-ds/compta-clair." >&2
    echo "  git clone https://github.com/analytics-ds/compta-clair.git .deploy" >&2
    exit 1
fi

echo "[1/4] Build Hugo"
rm -rf public
hugo --gc --minify --quiet

echo "[2/4] Synchronisation vers .deploy"
# --delete pour que les pages supprimees disparaissent du site ; .git, .nojekyll et README
# appartiennent au repo de deploiement, pas au build, donc on les preserve.
rsync -a --delete \
    --exclude '.git' \
    --exclude '.nojekyll' \
    --exclude 'README.md' \
    public/ "$DEPLOY/"

echo "[3/4] Controle de fuite"
# Garde-fou : certains mots ne doivent jamais atteindre un fichier public. Un commentaire
# oublie dans un CSS ou un template suffirait a exposer la nature du site (deja arrive le
# 2026-09-18, l'en-tete de main.css citait un terme interne).
# La liste vit dans .claude/leak-terms.txt, hors depot, pour ne pas publier les mots eux-memes.
# -I : ignorer les binaires, dont les octets d'un .webp peuvent contenir un terme par hasard.
TERMS_FILE="$ROOT/.claude/leak-terms.txt"
if [ ! -f "$TERMS_FILE" ]; then
    echo "ERREUR : $TERMS_FILE introuvable (il est hors depot, le recuperer sur le Drive)." >&2
    exit 3
fi
LEAKS=$(grep -rlIif "$TERMS_FILE" "$DEPLOY" --exclude-dir=.git || true)
if [ -n "$LEAKS" ]; then
    echo "ERREUR : termes internes trouves dans les fichiers a publier :" >&2
    echo "$LEAKS" >&2
    echo "Corriger a la SOURCE (theme, layouts, content) puis relancer." >&2
    exit 2
fi

echo "[4/4] Commit et push"
cd "$DEPLOY"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
    echo "Rien a publier, le site en ligne est deja a jour."
    exit 0
fi
git add -A
git commit -q -m "$MESSAGE"
git push -q origin main

echo
echo "Publie : https://analytics-ds.github.io/compta-clair/"
echo "GitHub Pages met ~1 minute a reconstruire."
