# sentiment-app : TP1 à TP5

Application du module *Développement et déploiement d'applications intelligentes*, mise à jour selon le guide de rattrapage d'octobre 2026. Le modèle TF-IDF et régression logistique classe les avis clients ; sous le seuil de confiance de 0,60, l'API répond `INDETERMINE` et demande une vérification humaine.

| TP | Réalisation | Compte rendu |
| --- | --- | --- |
| TP1 | Environnement Python 3.11, Git et trois fiches de cadrage | [Fiches](docs/cadrage/) |
| TP2 | Entraînement, évaluation et prédiction reproductibles | [Semaine 2](docs/semaine2.md) |
| TP3 | API FastAPI : `/health`, `/predict`, `/docs` | [Semaine 3](docs/semaine3.md) |
| TP4 | Contrat, abstention, jeu d'or, intégration et qualité | [Semaine 4](docs/semaine4.md) |
| TP5 | Interface Streamlit cliente de l'API, avis seul et CSV | [Semaine 5](docs/semaine5.md) |

Le [journal de rattrapage](docs/journal-tp1-tp5.md) distingue les contrôles rejoués des vérifications à faire par chaque membre sur son poste. Les documents de l'ancienne version où le TP3 était une interface directe restent dans [les archives](docs/archives/) et [les anciens comptes rendus](docs/comptes-rendus/).

## Installation sous PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
python scripts/check_setup.py
python src/make_demo.py
python src/train.py
python src/evaluate.py
pre-commit install
```

`requirements.txt` contient les dépendances de tout le semestre. Le verrou `requirements.lock` enregistre les versions installées sur le poste Windows. La contrainte directe `pyarrow==21.0.*` a été retirée conformément au guide pour laisser MLflow et Streamlit sélectionner une version compatible.

L'entraînement par défaut utilise les 290 avis de démonstration, comme la CI et les tests des TP3 à TP5. L'option `python src/train.py --allocine` permet l'expérience du TP2 sur les 20 000 avis Allociné ; relancer ensuite `python src/train.py` avant les vérifications de l'API et du jeu d'or.

`models/sentiment.joblib`, les données générées, `.venv/` et `.env` sont ignorés par Git. Seules les métriques et les petits jeux d'évaluation sont versionnés.

## Démarrer les deux applications

Dans deux terminaux, depuis la racine du dépôt, avec `.venv` activé :

```powershell
# Terminal 1 : API et documentation interactive
uvicorn api.main:app --reload
# http://127.0.0.1:8000/docs
```

```powershell
# Terminal 2 : interface
streamlit run ui/app.py --server.headless true
# http://localhost:8501
```

L'interface envoie des requêtes HTTP ; elle ne charge jamais le modèle. `API_URL` permet de choisir l'adresse du service. L'onglet CSV attend une colonne `text` ; [data/avis_exemple.csv](data/avis_exemple.csv) contient six exemples.

## Vérifier et afficher l'avancement

Le [pas-à-pas pour la présentation au professeur](docs/presenter-au-prof.md)
donne chaque commande, les résultats attendus et les essais dans le navigateur.

Dernière vérification locale : **102 tests réussis, 4 erreurs connues attendues**,
aucun échec ni test ignoré ; couverture de l'API **97,70 %**.
La CI sur clone neuf a également réussi. Le journal conserve les mesures et les
points nécessitant encore la validation du binôme.

```powershell
git log --oneline -10
git status
python -m pytest -q
python -m pytest tests/ -v
python -m pytest tests/test_api.py -q
python -m pytest tests/test_limites.py -q
python -m pytest tests/test_jeu_or.py -q
python -m pytest tests/test_client.py -q
ruff check .
mypy api
python -m pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
python src/courbe_seuil.py
python src/bilan_jeu_or.py
```

La CI entraîne le modèle de démonstration avant les tests, puis exécute ruff, mypy et pytest avec au moins 95 % de couverture de l'API. Les erreurs connues du jeu d'or restent documentées et sont attendues avec `xfail(strict=True)`.

## Membres du binôme

| Rôle | Nom | GitHub |
| --- | --- | --- |
| Membre A | Othmane Moussawi | @OthmaneW37 |
| Membre B | Ahmed Rayane Ramzi | @RayaneRZ24 |

Chaque membre doit refaire les essais sur son poste et commiter sous son identité.
