#!/bin/bash
# deploy-pages.sh
# Publie le site sur GitHub Pages : https://les-cles-du-dirigeant.fr/
#
# C'est LE moyen de publier ce site : il n'y a pas de build automatique.
#
# Le depot a deux branches :
#   main      = la source Hugo (content, themes, data...), ce que recupere un collaborateur
#   gh-pages  = le site construit, la seule branche servie par GitHub Pages
#
# Ce script construit le site et pousse le resultat sur gh-pages via le clone `.deploy/`.
# La source, elle, se commite a la main sur main.
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
    echo "ERREUR : $DEPLOY n'est pas un clone de analytics-ds/les-cles-du-dirigeant." >&2
    echo "  git clone https://github.com/analytics-ds/les-cles-du-dirigeant.git .deploy" >&2
    exit 1
fi

echo "[1/5] Build Hugo"
rm -rf public
hugo --gc --minify --quiet

echo "[2/5] Index de recherche Pagefind"
# Hugo ne genere pas l'index : sans cette etape, public/ n'a pas de dossier pagefind/, le rsync
# --delete l'efface de gh-pages et la recherche du site repond 404 (constate le 2026-09-21).
npx -y pagefind@1 --site public >/dev/null

echo "[3/5] Synchronisation vers .deploy"
# Le clone .deploy doit etre sur gh-pages AVANT le rsync --delete, sinon on ecrase la source
# de main avec le site construit et le checkout suivant part en vrille.
git -C "$DEPLOY" fetch -q origin gh-pages
git -C "$DEPLOY" checkout -q gh-pages 2>/dev/null || git -C "$DEPLOY" checkout -q -b gh-pages origin/gh-pages
git -C "$DEPLOY" reset -q --hard origin/gh-pages
# --delete pour que les pages supprimees disparaissent du site ; .git, .nojekyll et README
# appartiennent au repo de deploiement, pas au build, donc on les preserve.
rsync -a --delete \
    --exclude '.git' \
    --exclude '.nojekyll' \
    --exclude 'README.md' \
    public/ "$DEPLOY/"

echo "[4/5] Controle de fuite"
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

echo "[5/5] Commit et push"
cd "$DEPLOY"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
    echo "Rien a publier, le site en ligne est deja a jour."
    exit 0
fi
git add -A
git commit -q -m "$MESSAGE"
git push -q origin gh-pages

echo
echo "Publie : https://les-cles-du-dirigeant.fr/"
echo "GitHub Pages met ~1 minute a reconstruire."
