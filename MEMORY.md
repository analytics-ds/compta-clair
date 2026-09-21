# Suivi des publications — Les Clés du Dirigeant

Trace tous les articles publiés, classés par semaine. Limite : 4 articles/semaine/blog. Mis à jour automatiquement par `/create-article-geo`.

## 2026-09-21 — La source est sur GitHub, le depot a deux branches

Jusqu'au 2026-09-21, le depot `analytics-ds/les-cles-du-dirigeant` ne contenait que le site construit,
et la source ne vivait que sur le Drive, sans historique. Un collaborateur ne pouvait rien
produire a partir de GitHub.

- La source complete est desormais sur la branche **`main`**.
- Le site construit vit sur la branche **`gh-pages`**, seule branche servie par GitHub Pages.
- **Pas de GitHub Actions sur ce site**, choix assume. Publier = `deploy-pages.sh`, qui
  construit et pousse sur `gh-pages`. La source se commite separement sur `main`.
- Le theme a ete renomme (voir l'entree suivante) : son ancien nom etait un terme interne et
  partait dans `hugo.toml`, donc sur un depot public.
- Restent hors depot (`.gitignore`) : `CAHIER-DES-CHARGES.md` et `.claude/leak-terms.txt`.
  Ne jamais les committer.
- Deux gestes au lieu d'un : oublier de pousser `main` fait diverger le depot du dossier de
  travail. C'est le principal risque de cette organisation.

## 2026-09-21 — Le media s'appelle Les Cles du Dirigeant, logo pose, 3 bugs corriges

Le site avait ete developpe sous un nom provisoire. Renommage complet en **Les Clés du Dirigeant**,
identite visuelle posee, et trois bugs corriges au passage.

- **Nom.** Remplace partout dans `content/`, `data/`, `static/llms.txt`, `hugo.toml`, le theme et
  la doc. Les tournures contractees sont traitees a la main, « de Compta Clair » devient
  « des Clés du Dirigeant », jamais « de Les Clés du Dirigeant ». Le theme est renomme
  `themes/les-cles-du-dirigeant`.
- **Logo.** Le fichier fourni etait un PNG encapsule dans un SVG (1,1 Mo, fond blanc opaque).
  Vectorise par couche de couleur, 21 Ko. `static/images/logo.svg` est le lockup horizontal du
  header, `logo-dark.svg` sa version pour fond sombre, `logo-vertical.svg` sert au JSON-LD.
  Favicon simplifie a la cle seule, le lockup complet etant illisible sous 32 px. Palette du
  logo, marine `#032247` et or `#B98F23`.
- **Toutes les pages EN sortaient avec le chrome francais.** Le test de langue des templates,
  `strings.HasPrefix .RelPermalink "/en/"`, ne peut pas marcher tant que le site vit sous
  `/compta-clair/` : le permalien commence par le chemin du site. Verifie en ligne, la page EN
  affichait « Navigation principale » et FR comme langue courante. Le test retire desormais le
  chemin de base avant la comparaison, 18 occurrences corrigees dans le theme. Statut, **resolu**.
- **hreflang et selecteur de langue.** La version EN etait annoncee `hreflang="fr"`, chaque page
  portait deux alternates `fr`, `x-default` pointait sur la page courante au lieu du FR, et le
  lien EN du header visait la racine du domaine au lieu du site. Meme cause pour les trois, plus
  un `absURL` sur un chemin a slash initial qui perd le prefixe du site. Statut, **resolu**.
- **og:image et logo du JSON-LD.** `default_og_image` et `logo` etaient ecrits avec un slash
  initial, donc `absURL` les sortait sans le prefixe du site, et `static/images/og-default.jpg`
  n'existait meme pas. Chemins passes en relatif et image de partage creee. Statut, **resolu**.

**Reste a faire, en un seul passage, le jour ou le domaine definitif est connu** (voir la section
suivante) : `baseURL`, `noindex = false`, les URLs absolues de `robots.txt` et `llms.txt`,
l'adresse e-mail de `content/contact.md` et `content/en/contact.md` qui est encore sur l'ancien
nom de domaine, `static/CNAME`, le renommage du depot, et la pose du domaine custom par l'API
Pages avec le compte `analytics-ds` (le fichier CNAME seul ne suffit pas en deploiement Actions).

## 2026-09-21 — Bascule sur le domaine les-cles-du-dirigeant.fr

- `baseURL`, `static/robots.txt`, `static/llms.txt` et les adresses e-mail des pages contact FR
  et EN sont passes sur `https://les-cles-du-dirigeant.fr/`. `static/CNAME` pose, sans saut de
  ligne final, pour que le domaine custom survive au rsync du deploiement.
- **`noindex` reste a `true`** tant que le DNS ne pointe pas sur GitHub Pages et que le
  certificat n'est pas delivre. Sinon c'est l'URL github.io qui se ferait indexer, et il faudrait
  gerer une migration. Le passage a `false` est le dernier geste, apres verification par `dig`.
- **La recherche du site etait cassee en ligne** : `deploy-pages.sh` ne generait pas l'index
  Pagefind, et son `rsync --delete` effacait a chaque publication le dossier `pagefind/` de
  `gh-pages`. Verifie, `pagefind/pagefind-ui.js` repondait 404. Une etape `npx pagefind` est
  ajoutee au script, avant la synchro. Statut, **resolu**.
- **`deploy-pages.sh` basculait `.deploy` sur `gh-pages` apres le rsync**, donc il synchronisait
  le site construit par-dessus la source de `main` avant de changer de branche. Le checkout et
  un `reset --hard origin/gh-pages` passent desormais avant la synchro. Statut, **resolu**.
- L'adresse `redaction@les-cles-du-dirigeant.fr` est affichee sur les pages contact. **La boite
  n'existe pas encore**, elle est a creer chez le registrar ou le fournisseur de messagerie.

## A REPRENDRE — remettre le site en index (bloquant pour le SEO)

**Depuis le 2026-09-18, tout le site est en `noindex, nofollow`.** C'est volontaire : il vit sur
`https://les-cles-du-dirigeant.fr/`, une URL provisoire. Le laisser s'indexer la
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
