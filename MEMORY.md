# Suivi des publications — Compta Clair

Trace tous les articles publiés, classés par semaine. Limite : 4 articles/semaine/blog. Mis à jour automatiquement par `/create-article-geo`.

## 2026-09-21 — La source est sur GitHub, le deploiement passe par Actions

Jusqu'au 2026-09-21, le depot `analytics-ds/compta-clair` ne contenait que le site construit,
et la source ne vivait que sur le Drive, sans historique. Un collaborateur ne pouvait rien
produire a partir de GitHub.

- La source complete est desormais poussee sur `main`, comme le reste du parc.
- GitHub Pages est passe en mode **GitHub Actions** : `.github/workflows/hugo.yml` construit
  (Hugo 0.166.0 + Pagefind) et publie a chaque push. **Ne plus lancer `deploy-pages.sh` par
  reflexe**, il ne sert plus qu'en secours si Actions est indisponible.
- Le theme a ete renomme `pbn-expertise-comptable` vers `compta-clair` : son ancien nom
  partait dans `hugo.toml`, donc sur un depot public.
- Restent hors depot (`.gitignore`) : `CAHIER-DES-CHARGES.md` et `.claude/leak-terms.txt`.
  Ils nomment le client et les termes interdits. Ne jamais les committer.
- Le Drive et GitHub portent maintenant le meme contenu. Les faire diverger est le principal
  risque de cette organisation : commiter et pousser apres chaque session de production.

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
