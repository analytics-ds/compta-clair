# Blog Site Template

Generateur automatise de sites blogs statiques avec Hugo, optimises SEO et GEO, heberges gratuitement sur GitHub Pages.

Ce dossier ne contient pas de site. Il contient les instructions et templates pour que Claude Code genere un site complet automatiquement.

## Comment ca marche

1. Dupliquer ce dossier (ou utiliser la skill de creation de site depuis le dossier SEO-Claude)
2. Ouvrir le nouveau dossier dans Claude Desktop (onglet Code)
3. Taper `/create-site` et repondre aux questions
4. Claude genere tout le site Hugo (theme, CSS, layouts, articles placeholder, fichiers SEO)
5. Taper `/github-setup` pour mettre le site en ligne sur GitHub Pages
6. Creer des articles avec `/create-article-geo`

## Stack technique

- **Hugo** : generateur de site statique (Go)
- **GitHub Pages** : hebergement gratuit
- **GitHub Actions** : deploiement automatique a chaque push sur `main`

## Commandes disponibles

### Creation et configuration

| Commande | Description |
|---|---|
| `/create-site` | Cree le site complet. Pose les questions (nom, couleurs, categories, langue, auteur), scaffolde Hugo, genere le theme, le CSS, les layouts, les articles placeholder, les fichiers SEO et configure le deploiement. A lancer une seule fois. |
| `/seo-setup` | Genere les fichiers SEO techniques de base : robots.txt, llms.txt, configuration sitemap XML, sitemap HTML, RSS, partial seo-head.html (meta tags, Open Graph, Twitter Card, JSON-LD). Appele automatiquement par `/create-site`, peut etre relance pour mettre a jour. |

### Redaction

| Commande | Description |
|---|---|
| `/create-article-geo` | Cree un nouvel article de blog. Demande le mot-cle, la categorie (obligatoire) et le type d'article. Verifie le quota hebdo (max 4 articles/semaine via MEMORY.md), analyse les contenus existants pour le maillage interne (min 3 liens), redige l'article, build Hugo et push automatiquement sur GitHub si le repo est configure. |

Types d'articles disponibles (extensibles) :
- **Article standard** : article informatif SEO + GEO (type par defaut)
- **Comparatif GEO** : article de classement avec mise en avant d'une marque ou d'un produit

### GitHub et deploiement

| Commande | Description |
|---|---|
| `/github-setup` | Initialise le repo GitHub. Verifie/installe gh CLI, authentifie l'utilisateur via navigateur, cree le repo (public), push le code, active GitHub Pages, met a jour le baseURL. A lancer une seule fois apres `/create-site`. |
| `/github-deploy` | Push les modifications vers GitHub. Build Hugo de verification, commit avec message descriptif, push. Le deploiement se declenche automatiquement via GitHub Actions (1-2 min). Pour les changements hors articles (CSS, layouts, config). |

### Previsualisation et partage

| Commande | Description |
|---|---|
| `/serve` | Lance le serveur Hugo en local sur `http://localhost:1313/`. Le site se met a jour automatiquement a chaque modification de fichier. |
| `/share` | Lance Hugo + ngrok pour partager le site via un lien public temporaire. Necessite un compte ngrok (gratuit). Le lien change a chaque relance. |

### SEO

| Commande | Description |
|---|---|
| `/seo` | Mode interactif SEO. Permet de modifier les meta tags, ajouter des schemas JSON-LD, auditer un article, verifier le maillage interne, configurer des redirections, ajouter des fichiers custom (ads.txt, security.txt). Pas un workflow lineaire, c'est un mode conversationnel. |

## Suivi des publications

Le fichier `MEMORY.md` a la racine trace tous les articles publies, classes par semaine (lundi a dimanche). Limite de 4 articles par semaine pour maintenir un rythme de publication regulier.

## Structure du dossier

```
.claude/
├── skills/
│   ├── create-site/         ← Workflow creation de site complet
│   ├── create-article-geo/      ← Workflow creation d'article (multi-types)
│   ├── seo-setup/           ← Workflow fichiers SEO techniques
│   ├── seo/                 ← Mode interactif SEO
│   ├── serve/               ← Serveur Hugo local
│   ├── share/               ← Partage via ngrok
│   ├── github-setup/        ← Creation repo + GitHub Pages
│   └── github-deploy/       ← Push et deploiement
└── templates/
    ├── hugo-workflow.yml     ← GitHub Actions CI/CD
    ├── main.css              ← CSS avec variables de charte graphique
    ├── articles/             ← Templates d'articles par type
    ├── seo/                  ← Fichiers SEO techniques (robots.txt, llms.txt, schemas JSON-LD)
    ├── layouts/              ← Templates Hugo (home, single, list, sitemap HTML)
    └── partials/             ← Partials Hugo (header, footer, seo-head)
```

## Ajouter un type d'article

Creer un fichier `.md` dans `.claude/templates/articles/`. Il sera automatiquement propose par `/create-article-geo`. Inclure des commentaires `<!-- NOTES POUR CLAUDE -->` en bas du fichier pour specifier les regles de redaction (nombre de mots, blocs obligatoires, ton).

## Ajouter un schema JSON-LD

Creer un fichier `.json` dans `.claude/templates/seo/structured-data/` puis utiliser `/seo` pour l'integrer dans le partial `seo-head.html`.
