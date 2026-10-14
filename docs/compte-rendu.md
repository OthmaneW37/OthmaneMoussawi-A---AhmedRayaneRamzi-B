# Compte rendu global des TP1 à TP3

**Binôme :** Othmane Moussawi (@OthmaneW37) et Ahmed Rayane Ramzi (@RayaneRZ24)
**Dépôt :** https://github.com/OthmaneW37/OthmaneMoussawi-A---AhmedRayaneRamzi-B
**Date :** 14/10/2026

## 1. Le besoin et son cadrage

Une équipe relation client reçoit plusieurs milliers d'avis par jour et les traite dans l'ordre d'arrivée : un client mécontent peut donc attendre derrière des dizaines de clients satisfaits. Le besoin n'est pas de « comprendre » les avis, mais de les **trier** pour faire remonter les négatifs en tête de file. Le coût d'un retard est réel (client perdu, avis public dégradé), le coût d'une erreur de tri reste limité.

Pour le cas 3, nous avons retenu le **machine learning**, en suivant l'arbre de décision dans l'ordre. Il n'existe pas de logique connue et stable pour reconnaître un avis négatif : une liste de mots-clés échoue dès qu'apparaissent une négation (« pas déçu ») ou un retournement (« bien emballé, mais cassé »), donc les règles métier sont écartées. En revanche, **(a)** les données étiquetées sont gratuites : chaque avis arrive avec une note en étoiles qui fournit l'étiquette, ce qui ouvre directement la voie à l'apprentissage supervisé. **(c)** Le volume, des milliers d'avis par jour, impose un coût par requête quasi nul, ce qu'un classifieur TF-IDF plus régression logistique offre (quelques millisecondes sur un CPU) et qu'un modèle génératif appelé par API n'offre pas. **(d)** La conséquence d'une erreur est faible : un avis mal classé est traité plus tard, pas perdu, ce qui rend acceptable un modèle statistique imparfait. **(b)** La vérifiabilité n'est pas un frein : on ne demande pas de justifier chaque décision, seulement que la file soit mieux ordonnée qu'au hasard. Le RAG ne s'applique pas, puisqu'il n'y a aucun document à citer.

Les deux autres fiches illustrent ce que le ML n'est pas : le cas 1 (ordonnances incomplètes) relève des **règles métier**, car la liste des mentions obligatoires est réglementaire, il n'y a pas d'étiquettes (a) et une erreur est grave (d) ; le cas 2 (règlement intérieur) relève du **RAG**, parce que la réponse doit citer l'article (b) et qu'il n'existe pas de questions-réponses étiquetées (a).

## 2. L'architecture du dépôt

| Dossier | Contenu | Versionné ? |
| --- | --- | --- |
| `docs/` | Fiches de cadrage (`cadrage/cas1` à `cas3`), `semaine2.md`, `semaine3.md`, ce compte rendu | Oui |
| `src/` | `make_demo.py`, `train.py`, `evaluate.py`, `predict.py` (TP2) | Oui |
| `ui/` | `helpers.py` (logique testable) et `app.py` (affichage Streamlit) (TP3) | Oui |
| `tests/` | 45 tests : environnement (23), cadrage (12), Git (3), modèle (4), interface (3) | Oui |
| `scripts/` | Diagnostic `check_setup.py`, installation `setup.ps1` / `setup.sh`, `verif_clone.sh` | Oui |
| `.github/workflows/ci.yml` | Intégration continue : rejoue les tests à chaque push sur une machine neuve | Oui |
| `data/` | `sample_reviews.csv` versionné ; `demo_reviews.csv` régénéré par `make_demo.py` | En partie |
| `models/` | `metrics.json` versionné ; `sentiment.joblib` produit localement | En partie |
| `.venv/` | L'environnement Python | Non |

La règle est simple : **ce qui se reconstruit par une commande ne va pas dans Git**. L'environnement se recrée avec `pip install -r requirements.txt`, le jeu de démonstration avec `python src/make_demo.py`, le modèle avec `python src/train.py`. Les versionner ferait gonfler le dépôt à chaque réentraînement (le `.joblib` Allociné, avec ses 149 529 termes de vocabulaire, pèse plusieurs mégaoctets) sans rien apporter.

**Pourquoi `models/metrics.json` est-il dans Git alors que `models/sentiment.joblib` ne l'est pas ?** Parce que la mesure est la **preuve** de la qualité, et qu'elle ne se reconstruit pas sans réentraîner. La CI n'a jamais le modèle : les deux tests qui appellent `predict()` y sont ignorés, mais les deux tests qui lisent `metrics.json` y tournent et vérifient que le F1 dépasse le seuil de 0,85 inscrit à côté de la mesure. On transporte la preuve, pas l'artefact. C'est l'exception `!models/metrics.json` ajoutée au `.gitignore` par le kit du TP2 qui le permet.

## 3. Le modèle

**Données.** Deux jeux : le jeu de démonstration généré par `make_demo.py` (290 avis, 145 positifs et 145 négatifs, dont 100 mitigés et 30 neutres) et le jeu public Allociné (20 000 critiques de films, dont 10 204 négatives).

**Découpage.** `train_test_split` avec `test_size=0.2`, `stratify` sur l'étiquette et `random_state=42`, appliqué **avant** toute vectorisation. Si l'on vectorisait d'abord, le TF-IDF calculerait ses fréquences de documents sur le jeu de test : le vocabulaire et les poids contiendraient de l'information sur des avis censés n'avoir jamais été vus, et le score serait optimiste. La graine fixe rend le découpage identique d'une exécution à l'autre, et `evaluate.py` reproduit exactement le même découpage en réimportant `GRAINE` depuis `train.py`.

**Pipeline.** Un `Pipeline` scikit-learn qui enchaîne `TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)` et `LogisticRegression(class_weight="balanced")`. Sauvegarder le pipeline entier, et pas seulement le classifieur, garantit que la même transformation s'applique à l'entraînement et en production : `predict()` reçoit du texte brut.

**Résultats** (valeurs de nos exécutions ; le `metrics.json` versionné est celui d'Allociné) :

| Jeu | Avis | Vocabulaire | F1 macro | Exactitude | Rappel négatif |
| --- | --- | --- | --- | --- | --- |
| Démonstration | 290 (232 / 58) | 316 termes | 0,879 | 0,879 | 0,931 |
| Allociné | 20 000 (16 000 / 4 000) | 149 529 termes | 0,9205 | 0,9205 | 0,9113 |

Nos chiffres sont identiques à ceux du kit de référence (0,879 et 0,920), ce qui est attendu : les données de démonstration sont générées avec une graine fixe, Allociné est un fichier figé, et le découpage est déterministe.

**Matrice de confusion, jeu de démonstration** (lignes = vérité, colonnes = prédiction) :

```text
            negative  positive
  negative        27         2
  positive         5        24
```

Ligne `negative` : sur 29 avis réellement négatifs, 27 sont bien remontés et **2 sont classés positifs** ; ce sont les erreurs qui coûtent, deux clients mécontents qui attendront. Ligne `positive` : sur 29 avis positifs, 24 sont reconnus et 5 sont classés négatifs ; ces erreurs-là font seulement perdre un peu de temps à un agent. Le modèle penche donc vers « négatif » (32 prédictions négatives pour 29 réelles), ce qui va dans le bon sens pour le métier.

**Matrice de confusion, Allociné** (4 000 avis de test) :

```text
            negative  positive
  negative      1860       181
  positive       137      1822
```

318 erreurs sur 4 000 (7,95 %). Ici le rapport s'inverse : 181 négatifs manqués pour 137 positifs classés négatifs, d'où un rappel négatif (0,911) légèrement inférieur au rappel positif (0,930). Sur des critiques de films longues, l'ironie et les phrases concessives (« malgré un casting prestigieux… ») trompent le modèle plus souvent dans ce sens.

Le modèle n'a pas changé entre les deux jeux : ce sont les données qui font la différence. Le F1 passe de 0,879 à 0,920, et surtout la mesure devient crédible : sur 58 avis, une seule erreur de plus fait bouger le F1 de près de deux points ; sur 4 000, la mesure est stable.

## 4. L'analyse des erreurs

Sur le jeu de démonstration, les **7 erreurs sont toutes des avis mitigés**. En voici trois, tirées de notre exécution de `evaluate.py`, avec la confiance du modèle :

| Vérité | Prédit | Confiance | Avis |
| --- | --- | --- | --- |
| negative | positive | 0,56 | « Service impeccable et livraison en avance sur le papier, sauf que ensuite produit cassé à l'arrivée. » |
| positive | negative | 0,53 | « Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme à la description, très satisfait. » |
| negative | positive | 0,69 | « Service impeccable et livraison en avance les premiers jours, avant que notice incompréhensible et pièces manquantes. » |

**Le mécanisme.** Chaque avis mitigé est construit en deux moitiés de sentiments opposés reliées par un retournement (« sauf que ensuite », « mais finalement »), et l'étiquette suit la seconde moitié, celle qui conclut. Or le TF-IDF est un **sac de mots** : il compte les termes et leurs bigrammes, mais ne sait pas lequel vient en dernier. « Impeccable … puis cassé » et « cassé … puis impeccable » produisent presque le même vecteur. Le modèle additionne des indices positifs et négatifs de poids comparables, et tranche presque au hasard. Les bigrammes n'y changent rien : « sauf que » est un indice de retournement, pas de direction.

**Un signal utile.** Le modèle « sait » qu'il ne sait pas : sur les 7 erreurs, la confiance est comprise entre 0,53 et 0,69, alors qu'elle dépasse souvent 0,80 sur les avis nets. C'est exactement ce que le seuil d'incertitude du TP3 exploite.

**Pour les corriger,** il faudrait une représentation sensible à l'ordre et au contexte : des embeddings de phrase ou un modèle de type transformeur (prévu en semaine 9), qui donnent un poids différent à ce qui suit un « mais ». À plus court terme, ajouter des avis mitigés étiquetés aiderait un peu, tout comme des traits ad hoc (sentiment de la dernière proposition). Ce n'était pas le sujet de ces séances : l'objectif était un modèle reproductible et évalué honnêtement, dont on sait **pourquoi** il se trompe, pas un modèle optimal.

## 5. L'interface et le seuil d'incertitude

L'interface Streamlit (`ui/app.py`) n'écrit aucune logique de prédiction : elle appelle `predict()` du TP2 via `ui/helpers.py`, qui ajoute un verdict lisible (« positif », « négatif » ou « à vérifier »). Toute la logique est dans `helpers.py`, ce qui permet aux trois tests d'interface de tourner sans lancer Streamlit.

Effet du seuil mesuré sur les 4 000 avis de test Allociné :

| Seuil | Avis envoyés à un agent | Erreurs tranchées seules | dont négatifs manqués |
| --- | --- | --- | --- |
| 0,50 | 0 (0 %) | 318 | 181 |
| 0,55 | 249 (6,2 %) | 206 | 118 |
| **0,60** | **509 (12,7 %)** | **126** | **74** |
| 0,65 | 846 (21,1 %) | 76 | 43 |
| 0,70 | 1 183 (29,6 %) | 49 | 28 |
| 0,75 | 1 626 (40,6 %) | 27 | 17 |

**Nous retenons 0,60.** Ce seuil divise par 2,4 le nombre de négatifs que le modèle laisse passer seul (de 181 à 74), en échange d'environ un avis sur huit envoyé en relecture. Au-delà, le gain marginal se paie cher : passer à 0,75 évite encore 57 négatifs manqués, mais envoie 1 117 avis de plus à la file humaine ; pour une équipe qui reçoit des milliers d'avis par jour, l'automatisation perdrait alors son intérêt. Ce choix reste une proposition : le bon point dépend de la taille de l'équipe et du coût réel d'un client mécontent oublié, et il doit être arbitré avec l'équipe relation client, pas dans le code.

## 6. Ce qui a échoué

**Un environnement virtuel fantôme.** Le `.venv` du dépôt avait été créé dans un ancien emplacement (le dossier Téléchargements) puis le dépôt déplacé : `pyvenv.cfg` pointait vers un chemin qui n'existait plus et aucun paquet n'y était installé. Nous l'avons supprimé et recréé. Leçon : un venv n'est pas déplaçable, il se recrée, ce qui confirme qu'il n'a rien à faire dans Git.

**Pas de Python 3.11 sur le poste.** Seuls Python 3.12 et 3.13 étaient installés. Nous avons travaillé en 3.12 (le diagnostic l'accepte avec un avertissement), en installant seulement les paquets utiles aux trois TP plutôt que tout `requirements.txt` (mlflow, dvc, sentence-transformers sont prévus pour plus tard). La CI, elle, tourne bien en 3.11 : c'est elle qui garantit la compatibilité avec la version de référence. Un `OptimizeWarning` de scipy apparaît à l'entraînement avec cette combinaison de versions ; il est sans effet sur les résultats.

**Des fiches remplies… hors du dépôt.** Nos premières fiches de cadrage avaient été rédigées en dehors de `docs/cadrage/`, si bien que les fichiers versionnés sont restés vides et que `test_cadrage.py` est resté rouge (3 échecs au contrôle T1) alors que nous pensions l'étape terminée. Nous les avons réécrites directement dans `docs/cadrage/`, puis `pytest tests/test_cadrage.py` est passé à 12 tests verts.

**Un seul auteur de commits.** Le test `test_each_member_has_committed` a longtemps échoué : tous les commits portaient le même `user.name`. Ce test est le seul qui reste rouge tant que chaque membre n'a pas poussé un commit depuis son propre poste et son propre compte.

**Le changement de domaine au contrôle S2.** C'est l'échec le plus instructif. Avec le modèle entraîné sur Allociné, l'interface ne s'est pas comportée comme prévu : « Livraison rapide, produit conforme, je recommande. » est sorti « à vérifier » (positif à 59 %), « Produit cassé à l'arrivée et service client injoignable. » aussi (négatif à 58 %), et l'avis mitigé « Emballage soigné et notice claire, sauf que ensuite application qui plante. » a été tranché négatif à 65 % au lieu d'être signalé. Nous avons cru à un bug, puis réentraîné sur le jeu de démonstration pour comparer : là, les trois avis donnent 75 % positif, 85 % négatif et « à vérifier » à 52 %, exactement comme attendu. Le modèle Allociné a appris le vocabulaire des **critiques de films** (« scénario », « acteurs », « mise en scène ») et connaît mal celui du **e-commerce** (« livraison », « colis », « service client »). Sur `demo_reviews.csv`, il annonce 72,4 % de négatifs pour 50 % réels, et envoie 117 avis sur 290 à un agent au seuil de 0,60. Un F1 de 0,92 sur son propre jeu de test ne dit rien de sa qualité sur un autre domaine.

## 7. Ce que nous ferions autrement

Nous entraînerions le modèle sur des **avis e-commerce réels**, étiquetés par leur note en étoiles, plutôt que sur des critiques de films : le changement de domaine observé au TP3 montre que la meilleure métrique ne vaut que sur des données semblables à celles de production. Avec les moyens d'une vraie équipe, nous ajouterions un jeu de test métier figé, construit avec l'équipe relation client, et un suivi de la proportion d'avis « à vérifier » dans le temps comme premier indicateur de dérive. Enfin, nous fixerions l'environnement dès le premier jour (Python 3.11 installé sur tous les postes, un seul compte GitHub par poste) pour éviter les pertes de temps sur l'outillage.

## 8. Répartition du travail

| Membre | Ce qu'il a pris en charge |
| --- | --- |
| Othmane Moussawi | Création du dépôt et de l'environnement, fiches de cadrage, installation et exécution des kits TP2 et TP3, analyse des erreurs et du seuil, rédaction du compte rendu |
| Ahmed Rayane Ramzi | [À compléter par Ahmed Rayane Ramzi : ce qu'il a réellement fait] |

## Outils d'aide à la rédaction

Un assistant d'IA (Claude, d'Anthropic) a été utilisé pour exécuter les commandes des trois TP, rédiger les fiches de cadrage, `semaine2.md`, `semaine3.md` et une première version de ce compte rendu ; tous les chiffres cités proviennent des sorties réelles de `train.py`, `evaluate.py` et de `models/metrics.json`, que nous avons relues.
