# Hugo Site Factory

Ce repo est un template pour creer des sites blogs statiques avec Hugo, optimises SEO/GEO, heberges gratuitement sur GitHub Pages.

## Comment ca marche

Ce repo ne contient pas de site. Il contient les **instructions et templates** pour que Claude Code genere un site complet automatiquement.

### Premier lancement

1. L'utilisateur connecte Claude Code a ce repo
2. L'utilisateur tape `/create-site`
3. Claude pose les questions necessaires (nom du site, couleurs, categories, etc.)
4. Claude genere tout le site Hugo, les fichiers SEO, et configure le deploiement
5. L'utilisateur push sur GitHub, active GitHub Pages, le site est en ligne

### Utilisation courante

- `/create-article-geo` : creer un nouvel article de blog (choix parmi plusieurs types : article standard, comparatif). Push automatiquement sur GitHub si le repo est configure
- `/seo-setup` : generer ou mettre a jour les fichiers SEO techniques de base (robots.txt, llms.txt, sitemap, structured data)
- `/seo` : mode interactif pour modifier/ajouter des elements SEO (meta tags, JSON-LD, audit on-page, etc.)
- `/serve` : lancer le serveur Hugo en local (previsualisation sur `http://localhost:1313/`)
- `/share` : lancer Hugo + ngrok pour partager le site via un lien public (accessible par n'importe qui)
- `/github-setup` : creer un repo GitHub, push le code et activer GitHub Pages (mise en ligne du site)
- `/github-deploy` : push les modifications vers GitHub et declencher le deploiement

## Structure du repo

```
.claude/
├── scripts/
│   ├── deploy-pages.sh          ← Build + synchro + controle de fuite + push GitHub Pages
│   ├── fetch-image.sh           ← Openverse, HERITE DU TEMPLATE, PLUS UTILISE sur ce site
│   └── image-bank/              ← Banque d'images du site (Unsplash + Pexels, curee a la main)
│       ├── queries.yaml         ← Requetes de recherche par categorie
│       ├── common.py            ← Chemins, cles API, lecture/ecriture de l'index
│       ├── fetch-candidates.py  ← Candidats + planche-contact HTML a cocher
│       └── build-bank.py        ← Telecharge la selection, remplit data/image-bank.yaml
├── skills/
│   ├── create-site.md           ← Workflow creation de site complet
│   ├── create-article-geo.md        ← Workflow creation d'article (multi-types)
│   ├── seo-setup.md             ← Workflow fichiers SEO techniques (baseline)
│   ├── seo.md                   ← Mode interactif SEO (modifications ponctuelles)
│   ├── serve.md                 ← Lancer le serveur Hugo en local
│   ├── share.md                 ← Lancer Hugo + ngrok (partage public)
│   ├── github-setup.md          ← Creer un repo GitHub + activer GitHub Pages
│   └── github-deploy.md         ← Push et deployer sur GitHub Pages
└── templates/
    ├── data/
    │   ├── authors.yaml          ← 6 auteurs partages avec bios FR/EN, expertise, topics
    │   └── avatar-prompts.md     ← Prompts de generation des 6 avatars (Midjourney/DALL-E)
    ├── hugo-workflow.yml         ← GitHub Actions CI/CD
    ├── main.css                  ← Design system CSS complet (variables, composants, responsive, a11y)
    ├── articles/                 ← Templates d'articles par type
    │   ├── article-standard.md   ← Article informatif SEO + GEO (type par defaut)
    │   └── geo-comparatif.md     ← Article comparatif avec mise en avant
    ├── seo/                      ← Fichiers SEO techniques (editables)
    │   ├── robots.txt            ← Modele robots.txt
    │   ├── llms.txt              ← Modele llms.txt
    │   └── structured-data/      ← Schemas JSON-LD
    │       ├── article.json      ← Article (avec image et @id croise)
    │       ├── organization.json ← Organization (avec @id, logo, expertise)
    │       ├── author.json       ← Person (auteur)
    │       ├── breadcrumb.json   ← BreadcrumbList
    │       ├── website.json      ← WebSite (avec publisher @id)
    │       └── faq.json          ← FAQPage (genere auto depuis frontmatter)
    ├── layouts/
    │   ├── baseof.html           ← Layout de base (skip-to-content, fonts non-bloquantes, favicon)
    │   ├── home.html             ← Page d'accueil
    │   ├── list.html             ← Pages de liste
    │   ├── single.html           ← Page article (breadcrumb, TOC sticky, image hero, auteur, articles similaires)
    │   ├── sitemap-html.html     ← Page plan du site (liste toutes les pages)
    │   └── 404.html              ← Page 404 custom
    └── partials/
        ├── header.html           ← Header sticky (backdrop-filter, aria-labels, mobile menu)
        ├── footer.html           ← Footer (aria-label, lien plan du site)
        └── seo-head.html         ← Meta tags SEO complets + JSON-LD auto (OG avec image, Twitter, canonical, hreflang, author, article:section, FAQPage auto, Organization @id)
```

## Contexte du site

> Cette section est remplie automatiquement par le skill `/create-site`.
> Elle permet a Claude de connaitre le contexte du site pour les futures actions.

> **Cadrage editorial** : lire `CAHIER-DES-CHARGES.md` (sur le Drive, hors depot) AVANT `/create-site` et avant chaque `/create-article-geo`. Il fixe les categories, la DA, les auteurs, les pages (fiches auteurs, qui sommes-nous, charte editoriale) et le gabarit d'article (En bref, sommaire, tableaux, bloc sources). Il prime sur les valeurs par defaut du template.

- **Nom du site** : Les Clés du Dirigeant — **PROVISOIRE**, à valider par Augustin (voir "Points ouverts" du cahier des charges, sur le Drive). À changer partout où il apparaît : `hugo.toml` (`title`, descriptions), `content/{_index.md,en/_index.md}`, `content/{qui-sommes-nous,charte-editoriale,contact,mentions-legales}.md` + équivalents EN, `themes/les-cles-du-dirigeant/layouts/_default/home.html` (H1 hero), `static/llms.txt`, `static/robots.txt`.
- **Description (FR)** : Les Clés du Dirigeant explique la comptabilité, la fiscalité et la création d'entreprise en clair : guides pratiques, sourcés, à jour, pour dirigeants de TPE, indépendants et particuliers.
- **Description (EN)** : Les Clés du Dirigeant explains French accounting, taxation and business creation in plain language: practical, sourced, up-to-date guides for small business owners, freelancers and individuals.
- **URL** : `https://les-cles-du-dirigeant.fr/` (GitHub Pages, compte `analytics-ds`, repo `les-cles-du-dirigeant`, construit par GitHub Actions a chaque push). `baseURL` de `hugo.toml` à remplacer le jour où un vrai domaine est choisi.
- **Couleurs** : palette de reference (`--primary` #12433F vert sapin, `--accent` #9FE3D0 menthe, `--background` blanc, `--text` #0D1D2F bleu nuit). Voir `themes/les-cles-du-dirigeant/assets/css/main.css`.
- **Polices** : Plus Jakarta Sans (titres), Source Serif 4 (corps), Inter (UI/tableaux).
- **Langue principale** : fr (version EN en sous-dossier `/en/` active, `defaultContentLanguageInSubdir = false`).
- **Categories (FR ↔ EN)** : Créer son entreprise / Starting a business · Statuts juridiques / Legal structures · Micro-entreprise / Micro-business · Comptabilité / Accounting · Fiscalité de l'entreprise / Business taxation · Paie et social / Payroll and social charges · Gérer son entreprise / Running a business · Fiscalité des particuliers / Personal taxation · Expert-comptable et métiers / Accountants and professions. Mapping slugs + titres dans `data/categories.yaml`.
- **Auteur principal du site** : `camille-renaud` (les 3 autres : `julien-marchal`, `nadia-benali`, `antoine-leclerc` — voir `data/authors.yaml` ; ne jamais leur attribuer le titre reglemente d'"expert-comptable").

### Particularités techniques de ce site (à lire avant toute modification de template)

- **`categories` n'est pas une taxonomie Hugo** (contrairement au reste du template) : c'est une section de contenu ordinaire (`content/categories/`, `layouts/categories/list.html`). Raison et contournements documentés en tête de `hugo.toml`, `data/categories.yaml`, `data/articles.yaml` et `themes/les-cles-du-dirigeant/layouts/partials/category-url.html`.
- **Bug Hugo constaté sur ce site (0.139 à 0.166) : `.Section`/`.Type` valent `"en"` au lieu du vrai nom de section pour toute page EN**, et `.Site.RegularPages`/`.Site.Sections`/`.Site.GetPage`/`.Translations` ne permettent pas de reconstituer de façon fiable la liste des articles EN depuis une page EN. Contournement : `data/articles.yaml` (registre statique slug/catégorie/auteur par article) + résolution via `.Site.GetPage` sur un chemin de contenu **explicite** (`"blog/<slug>"` ou `"en/blog/<slug>"`), seule méthode fiable constatée. Voir les commentaires en tête de `_default/{home,authors,author,sitemap-html}.html` et `categories/list.html`.
- **`.Site.Language.Lang`, `.Site.LanguageCode`, `.Site.Menus.main`, `.Site.Params.*` ne sont pas fiables dans un `partial`** (retournent la valeur FR même sur une page EN) : `partials/header.html`, `footer.html`, `seo-head.html` déduisent donc la langue de `.RelPermalink` (préfixe `/en/`) plutôt que de `.Site.Language.Lang`, et le menu principal + les textes du footer sont codés en dur par langue plutôt que lus depuis `.Site.Menus`/`.Site.Params`.
- **Limite résiduelle assumée** : sur la page d'accueil EN (`/en/`, Kind="home") uniquement, `.Site.GetPage` échoue même avec un chemin explicite qui fonctionne à l'identique depuis toute autre page (articles, catégories, auteurs, `/en/blog/` — tous vérifiés OK). Conséquence : les sections "Derniers articles" / "Les essentiels" et le compte d'articles par catégorie n'apparaissent pas sur `/en/` (dégradation propre, pas d'erreur ni de contenu cassé). Toute la navigation réelle (menu, `/en/blog/`, `/en/categories/*`, `/en/authors/*`) fonctionne normalement. À ré-investiguer si une nouvelle version de Hugo corrige ce point — ne pas re-simplifier les contournements ci-dessus sans relire l'historique de debug (session du 2026-09-16).

## Suivi des publications (MEMORY.md)

Le fichier `MEMORY.md` a la racine trace tous les articles publies, classes par semaine. Il est mis a jour automatiquement par `/create-article-geo`.

**Limite de publication : 4 articles par semaine maximum.** Avant chaque creation d'article, le systeme verifie le quota. Si 4 articles sont deja publies dans la semaine en cours, l'utilisateur est averti.

Cette limite sert a eviter la publication en masse et a maintenir un rythme de publication regulier, ce qui est meilleur pour le SEO.

## Mise en ligne (specifique a ce site)

Le site est en ligne sur **https://les-cles-du-dirigeant.fr/** (compte GitHub
`analytics-ds`, repo `les-cles-du-dirigeant`).

**Le depot a deux branches, ne pas les confondre :**

| Branche | Contenu | Role |
|---|---|---|
| `main` | la source Hugo (content, themes, data, .claude...) | ce que recupere un collaborateur |
| `gh-pages` | le site construit | la seule branche servie par GitHub Pages |

**Il n'y a pas de build automatique** : pas de GitHub Actions sur ce site. Publier se fait en
deux gestes distincts.

1. Mettre le site en ligne (construit + pousse sur `gh-pages`) :

```bash
bash .claude/scripts/deploy-pages.sh "message de commit"
```

2. Partager la source (commit sur `main`, depuis un clone du depot) :

```bash
git add -A && git commit -m "message" && git push origin main
```

Oublier le second geste fait diverger le depot du dossier de travail : c'est le principal
risque de cette organisation.

Le script refuse de publier si un terme interne apparait dans un fichier a mettre en ligne
(liste dans `.claude/leak-terms.txt`, hors depot) — corriger alors **a la source**, jamais dans
`.deploy/`. Detail du flux et cas d'erreur : skill `/github-deploy`.

**Documents qui ne partent jamais sur GitHub** : le cahier des charges et la liste de termes
du controle de fuite sont exclus par `.gitignore` et vivent sur le Drive, aupres du dossier
client. Les recuperer la-bas avant toute session de production.

## Banque d'images (specifique a ce site)

Les hero d'article ne sont plus tires au hasard sur Openverse : ils viennent d'une banque
curee a la main, propre a ce site : deux sites qui affichent la meme photo, c'est une
empreinte retrouvable par recherche d'image inversee.

- **Index** : `data/image-bank.yaml` (une entree par image : categories, tags, alt FR/EN, credit, `used_by`).
- **Fichiers** : `static/images/banque/<categorie>-NN.webp`, 1200x675, WebP.
- **Sources** : Unsplash + Pexels, cles `UNSPLASH_ACCESS_KEY` / `PEXELS_API_KEY` lues dans
  `<drive>/.claude/secrets/.env` (jamais recopiees dans le code).

Recharger la banque (quand `stats` montre trop peu d'images libres dans une categorie) :

```bash
uv run .claude/scripts/image-bank/fetch-candidates.py    # candidats + planche-contact HTML
open .image-bank-tmp/planche-contact.html                # cocher les images a garder
uv run .claude/scripts/image-bank/build-bank.py ~/Downloads/selection.json
uv run .claude/scripts/image-bank/build-bank.py stats    # etat par categorie
```

Les requetes de recherche se modifient dans `.claude/scripts/image-bank/queries.yaml`.

**Apres chaque `build-bank.py`** : les nouvelles entrees ont `alt_fr: ""` et `alt_en: ""`.
Claude doit rediger les deux alt (max 125 caracteres, description de ce qu'on VOIT, pas du
sujet de l'article) en regardant chaque image. Une image sans `alt_fr` n'est pas tirable.

## Regles generales

- **Bilinguisme obligatoire (langue principale + EN)** : tous les blogs generes par ce template sont bilingues. La langue principale est servie a la racine (`/`), la version anglaise en sous-dossier `/en/`. Hugo gere le multilingue via la convention de dossiers `content/` (principale) et `content/en/` (anglais). Chaque article et page a une paire de fichiers avec un `translationKey` identique dans le frontmatter. Le header contient un language switcher automatique. Les balises hreflang sont generees automatiquement par le partial `seo-head.html`. **Ne JAMAIS generer un site ou un article dans une seule langue** — c'est systematiquement FR + EN (ou la langue principale + EN)
- Toujours utiliser `relURL` dans les templates Hugo pour les liens (compatibilite GitHub Pages)
- Les articles vont dans `content/blog/` (langue principale) et `content/en/blog/` (anglais)
- Les slugs sont en minuscules, sans accents, mots separes par des tirets
- Ne JAMAIS utiliser `&` dans les noms de categories ou de tags — toujours remplacer par "et" (Hugo genere un double tiret `--` dans le slug, ce qui casse les URLs)
- Le ton des articles est impersonnel (pas de je/tu/nous/vous) sauf instruction contraire
- Les specs d'article (mots minimum, H2, blocs obligatoires) dependent du type choisi — lire les `<!-- NOTES POUR CLAUDE -->` dans chaque template d'article
- Chaque article doit contenir au minimum 3 liens internes contextuels vers d'autres articles du blog. L'ancre de chaque lien doit contenir le mot-cle principal de l'article cible. **Maillage intra-langue uniquement** : un article FR ne mail que des articles FR, un article EN ne mail que des articles EN (le lien vers la traduction est gere par le language switcher du header)
- **Systeme d'auteurs partage** : 6 auteurs definis dans `data/authors.yaml` (copie depuis `.claude/templates/data/authors.yaml` a la creation du site). Chaque auteur a un id-slug, un nom, un type (person/organization), un avatar, des `jobTitle`/`role`/`bio` bilingues FR/EN, une liste d'`expertise` et une liste de `topics` (mots-cles pour la selection automatique). Les auteurs disponibles : `thomas-durand` (tech), `magalie-ergoz` (mode/beaute), `claire-beaumont` (maison/habitat), `laura-verdier` (sante/bien-etre), `kevin-moreau` (transport/mobilite), `sophie-martin` (finance/patrimoine)
- **Selection automatique de l'auteur** : dans le frontmatter d'un article, le champ `author` contient l'**ID slug** de l'auteur (ex: `author: thomas-durand`), pas son nom complet. La skill `/create-article-geo` selectionne automatiquement l'auteur le plus pertinent selon les `topics` et `expertise` qui matchent avec le sujet de l'article. Si aucun match clair, l'auteur principal du site (defini dans la section "Contexte du site" de ce CLAUDE.md) est utilise
- **Avatars des auteurs** : fichiers WebP 512x512 dans `static/images/authors/[id].webp`. Style unifie "flat illustration portrait". Prompts de generation documentes dans `.claude/templates/data/avatar-prompts.md`. Si l'avatar est manquant, un placeholder coloree avec la 1ere lettre du nom s'affiche
- **JSON-LD Author** : le partial `seo-head.html` genere automatiquement un schema.org/Person (ou Organization) complet depuis les donnees de `data/authors.yaml` (name, jobTitle, description, knowsAbout, image, sameAs, worksFor)
- **Bloc auteur en bas d'article** : le layout `single.html` affiche automatiquement un encart avec avatar, nom, role, bio complete et expertise de l'auteur, traduit dans la langue de l'article (FR ou EN)
- Les templates SEO dans `.claude/templates/seo/` sont editables par l'utilisateur — toujours lire la version en place avant de generer
- Pour ajouter un nouveau type d'article, creer un `.md` dans `.claude/templates/articles/` — il sera automatiquement propose par `/create-article-geo`
- Pour ajouter un schema JSON-LD, creer un `.json` dans `.claude/templates/seo/structured-data/` et utiliser `/seo` pour l'integrer
- Chaque article doit avoir un champ `lastmod` dans le frontmatter (= date de derniere modification). Il est utilise par le sitemap XML, le sitemap HTML et le schema JSON-LD
- Quand un article est modifie, toujours mettre a jour le champ `lastmod` avec la date du jour
- Le sitemap HTML (`/plan-du-site/`) se regenere automatiquement a chaque build Hugo
- Toujours build et verifier (`hugo`) avant de commit
- Chaque article doit avoir un champ `faq` dans le frontmatter (liste de questions/reponses) pour generer automatiquement le schema FAQPage JSON-LD. Minimum 3 questions
- Chaque article a une image hero OBLIGATOIRE, **tiree de la banque d'images du site** (`data/image-bank.yaml`, fichiers dans `static/images/banque/`). Si aucune image libre ne correspond a la categorie, `/create-article-geo` s'arrete et demande de recharger la banque : on ne telecharge jamais une image a la volee et on ne republie jamais une image deja utilisee
- Le frontmatter contient 3 champs lies a l'image : `image` (chemin Hugo), `imageAlt` (texte alternatif FR, max 125 car), `imageCredit` (attribution du photographe). Ces 3 champs sont remplis automatiquement par le script
- L'image est affichee : (1) dans les cards de la homepage et des pages de liste, (2) en bannière cote a cote avec le titre sur la page article, (3) dans og:image pour les partages sociaux, (4) dans le schema Article JSON-LD
- Le credit photo est affiche sous l'image de l'article (petite mention en italique alignee a droite). Obligatoire pour respecter les licences CC BY et CC BY-SA
- Les Google Fonts sont chargees en non-bloquant (media="print" + swap JS) pour de meilleures performances
- Le layout inclut un lien "Skip to content" pour l'accessibilite
- Les navigations ont des `aria-label` pour les lecteurs d'ecran
- Le CSS respecte `prefers-reduced-motion` pour desactiver les animations si l'utilisateur le demande
- Les articles affichent une table des matieres (TOC) sticky en sidebar, generee automatiquement par Hugo
- Les articles similaires sont affiches en bas de page, calcules par Hugo via la config `[related]` dans hugo.toml

## Comment repondre a l'utilisateur

- Tutoiement, ton decontracte
- Pas de jargon technique sans explication
- Reponses structurees avec listes a puces
- Pas d'emoji sauf demande explicite
