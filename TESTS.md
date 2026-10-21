# Vérifier les TP1 à TP5

Depuis la racine du dépôt, créer et activer `.venv`, puis installer les deux fichiers de dépendances :

```powershell
python -m pip install -r requirements.txt -r requirements-dev.txt
python scripts/check_setup.py
python src/make_demo.py
python src/train.py
```

L'API, les tests du jeu d'or et l'interface sont vérifiés avec le modèle de démonstration, comme dans la CI. Le modèle et les données générées ne doivent jamais être commités.

## Vérification complète

```powershell
.\scripts\verifier.ps1 -Detail
```

Le script interrompt le contrôle dès qu'une commande échoue. Il ne lance pas de serveur et ne modifie pas Git. L'entraînement actualise `models/metrics.json` et crée le modèle local ignoré par Git.

## Commandes séparées

```powershell
python -m pytest -q
python -m pytest tests/ -v
python -m pytest tests/test_api.py -q
python -m pytest tests/test_limites.py -q
python -m pytest tests/test_jeu_or.py -q
python -m pytest tests/test_integration.py -q
python -m pytest tests/test_client.py tests/test_interface.py -q
ruff check .
mypy api
python -m pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
```

Les tests HTTP utilisent `TestClient` avec son contexte de démarrage réel. Les tests de page utilisent `streamlit.testing.v1.AppTest`. Il n'est pas nécessaire de démarrer uvicorn ni Streamlit pour pytest. Hypothesis vérifie les textes Unicode et les blancs ; les propriétés doivent passer trois exécutions successives.

## Qualité à chaque commit

```powershell
pre-commit install
pre-commit run --all-files
```

Activer `.venv` avant de commiter : les hooks locaux utilisent `ruff` et `mypy` de cet environnement. La CI réentraîne le modèle, lance les deux outils puis impose 95 % de couverture de `api/`.

Les sorties et les limites des contrôles effectués sont consignées dans [le journal](docs/journal-tp1-tp5.md) et [les mesures TP4](docs/semaine4.md). Les anciens états attendus du TP1 seul sont conservés dans [l'ancien document](docs/archives/ancien-TESTS.md).
