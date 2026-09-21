---
description: Publie le site sur GitHub Pages (repo analytics-ds/compta-clair). Utiliser ce skill quand l'utilisateur demande de deployer, publier, push, ou mettre a jour le site en ligne.
user_invocable: true
---

# Skill : Deployer sur GitHub Pages

## Declenchement

L'utilisateur tape `/github-deploy` ou demande de deployer / publier / push / mettre en ligne.

## Le modele de deploiement de CE site

Contrairement au template de la factory, **on ne pousse jamais la source sur GitHub**.

- Le dossier de travail (sur le Drive) n'est PAS un repo git. Il contient le cahier des charges,
  le CLAUDE.md, le MEMORY.md et les scripts : autant de documents qui expliquent noir sur blanc
  la nature du site et le client concerne.
- Le seul repo git est `.deploy/`, un clone de `analytics-ds/compta-clair` (public) qui ne
  contient **que le site construit** : HTML, CSS, images. Pas de CI, pas de GitHub Actions.
- URL publique : https://analytics-ds.github.io/compta-clair/

Ne jamais proposer de `git init` a la racine, ni de pousser la source « pour avoir le build
automatique », ni de basculer le repo public sur la source. Si ce besoin se represente un jour,
ce sera en repo prive et rien d'autre.

## Deployer

```bash
bash .claude/scripts/deploy-pages.sh "message de commit"
```

Le script enchaine : build Hugo (`--gc --minify`), synchro de `public/` vers `.deploy/`,
**controle de fuite**, commit, push. GitHub Pages reconstruit en ~1 minute.

Messages de commit : "Ajoute l'article : [titre]", "Met a jour le SEO : [quoi]", "Corrige [quoi]".

## Si le controle de fuite echoue

Le script s'arrete (exit 2) et liste les fichiers a publier qui contiennent un terme interne.
La liste des termes vit dans `.claude/leak-terms.txt`, volontairement hors depot. C'est arrive
le 2026-09-18 : l'en-tete de `main.css` citait un terme interne et renvoyait au cahier des
charges, publie tel quel sur `/css/main.css`.

Marche a suivre :
1. **Corriger a la source** (theme, layouts, content, data) — jamais dans `.deploy/`, la synchro
   ecraserait le correctif au deploiement suivant.
2. Relancer le script.

Ne jamais contourner le garde-fou, ne jamais commiter depuis `.deploy/` a la main.

## Verifier apres coup

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://analytics-ds.github.io/compta-clair/
```

Afficher l'URL a l'utilisateur, et signaler les pages ajoutees ou supprimees.

## Points ouverts lies au deploiement

- `baseURL` de `hugo.toml` pointe sur l'URL GitHub Pages. Le jour ou un vrai domaine est choisi :
  le changer, rebuild complet, redeploiement — sinon les URLs absolues, le sitemap et les
  hreflang restent sur github.io.
- Le site est indexable (`robots.txt` en `Allow: /`). Si le domaine final doit arriver plus tard,
  se demander s'il ne vaut pas mieux bloquer l'indexation de la version github.io en attendant,
  pour eviter une migration d'URL et du contenu duplique.
