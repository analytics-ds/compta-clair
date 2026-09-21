# Suivi des publications — Compta Clair

Trace tous les articles publiés, classés par semaine. Limite : 4 articles/semaine/blog. Mis à jour automatiquement par `/create-article-geo`.

## 2026-09-21 — La source est sur GitHub, le depot a deux branches

Jusqu'au 2026-09-21, le depot `analytics-ds/compta-clair` ne contenait que le site construit,
et la source ne vivait que sur le Drive, sans historique. Un collaborateur ne pouvait rien
produire a partir de GitHub.

- La source complete est desormais sur la branche **`main`**.
- Le site construit vit sur la branche **`gh-pages`**, seule branche servie par GitHub Pages.
- **Pas de GitHub Actions sur ce site**, choix assume. Publier = `deploy-pages.sh`, qui
  construit et pousse sur `gh-pages`. La source se commite separement sur `main`.
- Le theme a ete renomme vers `compta-clair` : son ancien nom etait un terme interne et
  partait dans `hugo.toml`, donc sur un depot public.
- Restent hors depot (`.gitignore`) : `CAHIER-DES-CHARGES.md` et `.claude/leak-terms.txt`.
  Ne jamais les committer.
- Deux gestes au lieu d'un : oublier de pousser `main` fait diverger le depot du dossier de
  travail. C'est le principal risque de cette organisation.

## A REPRENDRE — remettre le site en index (bloquant pour le SEO)

**Depuis le 2026-09-18, tout le site est en `noindex, nofollow`.** C'est volontaire : il vit sur
`https://analytics-ds.github.io/compta-clair/`, une URL provisoire. Le laisser s'indexer la
obligerait, au moment du passage sur le vrai domaine, a gerer une migration d'URL et du contenu
duplique sur un site qui n'a aucune autorite a depenser pour ca.

**Des que le nom de domaine definitif est choisi, dans le meme passage :**

1. `hugo.toml` → `[params] noindex = false` (la balise est generee par `partials/seo-head.html`).
2. `hugo.toml` → `baseURL` sur le nouveau domaine.
3. Verifier les URLs absolues qui ne suivent pas `baseURL` : `static/robots.txt` (ligne Sitemap)
   et `static/llms.txt` (Sitemap + RSS).
4. Rebuild complet et `bash .claude/scripts/deploy-pages.sh`, puis verifier en ligne :
   `curl -s <domaine>/ | grep -o '<meta name=robots[^>]*>'` ne doit plus rien retourner.
5. Soumettre le sitemap dans la Search Console du nouveau domaine.

Tant que le point 1 n'est pas fait, **aucun article publie ne sera indexe** : inutile de
s'interroger sur les positions ou le trafic avant.

## Semaine du 2026-09-15 (création initiale du site)

Placeholder de lancement : 1 article par catégorie (9 catégories), en FR + EN, généré lors de `/create-site`. Ne compte pas dans le quota hebdomadaire habituel (création initiale, pas publication courante).

| Catégorie | Article FR | Article EN | Auteur | Featured |
|---|---|---|---|---|
| Créer son entreprise | [Obtenir son Kbis](content/blog/kbis-creation-entreprise.md) | [Getting your Kbis](content/en/blog/company-registration-kbis.md) | camille-renaud | ✅ |
| Statuts juridiques | [SAS ou SARL](content/blog/choisir-statut-juridique-sas-sarl.md) | [SAS or SARL](content/en/blog/choosing-sas-sarl-legal-structure.md) | camille-renaud | — |
| Micro-entreprise | [Seuils auto-entrepreneur 2026](content/blog/seuils-auto-entrepreneur-2026.md) | [Auto-entrepreneur thresholds 2026](content/en/blog/auto-entrepreneur-thresholds-2026.md) | camille-renaud | ✅ |
| Comptabilité | [Facturation électronique obligatoire](content/blog/facturation-electronique-obligatoire.md) | [Mandatory e-invoicing](content/en/blog/mandatory-e-invoicing-france.md) | julien-marchal | — |
| Fiscalité de l'entreprise | [CFE](content/blog/cfe-cotisation-fonciere-entreprises.md) | [CFE local business tax](content/en/blog/cfe-local-business-tax-france.md) | julien-marchal | ✅ |
| Paie et social | [Lire sa fiche de paie](content/blog/lire-fiche-de-paie.md) | [How to read a French payslip](content/en/blog/how-to-read-french-payslip.md) | nadia-benali | — |
| Gérer son entreprise | [Gérer sa trésorerie](content/blog/gerer-tresorerie-tpe.md) | [Managing cash flow](content/en/blog/managing-cash-flow-small-business.md) | julien-marchal | ✅ |
| Fiscalité des particuliers | [SCI et LMNP](content/blog/sci-lmnp-immobilier-locatif.md) | [SCI and LMNP](content/en/blog/sci-lmnp-rental-property-taxation.md) | antoine-leclerc | — |
| Expert-comptable et métiers | [Rôle de l'expert-comptable](content/blog/role-expert-comptable-professions-liberales.md) | [Role of chartered accountants](content/en/blog/role-of-chartered-accountant-professions.md) | nadia-benali | — |

**Prochaine étape recommandée** : utiliser `/create-article-geo` pour enrichir chaque catégorie (2-3 articles/catégorie visés par le template), en respectant le quota de 4 articles/semaine/blog.
