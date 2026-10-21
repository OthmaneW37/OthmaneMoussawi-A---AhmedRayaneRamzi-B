# Refaire les tests et présenter le projet

## 1. Préparer le terminal PowerShell

```powershell
cd "C:\Users\NITRO 5\Downloads\OthmaneMoussawi-A---AhmedRayaneRamzi-B"
.\.venv\Scripts\Activate.ps1
python --version
```

Attendu : Python 3.11.x. Si l'activation est bloquée, utiliser directement
`.\.venv\Scripts\python.exe` à la place de `python` dans les commandes suivantes.
Cela évite de changer la politique d'exécution du PC.

Sur un autre poste : créer `.venv` avec `py -3.11 -m venv .venv`, l'activer puis
installer `python -m pip install -r requirements.txt -r requirements-dev.txt`.

## 2. Afficher l'avancement et le diagnostic

```powershell
git log --oneline -20
git status
git shortlog -sn --all
python scripts/check_setup.py
```

Expliquer : le journal Git présente les changements réels ; plusieurs commits
peuvent être un découpage d'un même travail. Les noms de l'historique ne prouvent
pas que chaque membre a exécuté chaque TP sur son poste. Le diagnostic attendu
est `0 erreur(s), 0 avertissement(s)`.

## 3. Reconstruire le modèle et lancer les tests

```powershell
python src/make_demo.py
python src/train.py
python -m pytest -q
python -m pytest tests/ -v
```

Attendu : 290 avis générés, F1 macro 0,879, puis **102 passed, 4 xfailed**.
`-q` donne le résumé ; `-v` affiche chaque test. Les quatre `xfail` sont de vraies
erreurs du modèle conservées et déclarées dans le jeu d'or, avec un motif.
Ce ne sont pas quatre réussites. Avec `strict=True`, un cas corrigé doit être
réexaminé : sa réussite inattendue fait échouer la suite.

Le modèle doit être celui de démonstration pour ces tests. Si des tests sont
`skipped` faute de modèle, refaire `python src/train.py`.

## 4. Présenter les TP séparément

```powershell
python -m pytest tests/test_cadrage.py tests/test_environment.py tests/test_git_history.py -q
python -m pytest tests/test_model.py -q
python -m pytest tests/test_api.py -q
python -m pytest tests/test_limites.py -q
python -m pytest tests/test_integration.py -q
python -m pytest tests/test_abstention.py -q
python -m pytest tests/test_jeu_or.py -q
python -m pytest tests/test_client.py tests/test_interface.py -q
```

| Contrôle | Résultat attendu | Explication courte |
| --- | --- | --- |
| TP1 | 38 passed | Structure, cadrage et Git |
| Modèle TP2 | 4 passed | Métriques et format des prédictions |
| API TP3 | 6 passed | Routes et erreurs d'entrée |
| Limites TP4 | 11 passed | Frontières et propriétés Unicode |
| Intégration TP4 | 7 passed | Démarrage et pannes 503/500 |
| Abstention TP4 | 4 passed | Frontière de 0,60 et étiquettes |
| Jeu d'or TP4 | 17 passed, 4 xfailed | 20 avis et contrôle de complétude |
| Client et page TP5 | 12 passed | HTTP et affichage Streamlit |

Trois tests historiques supplémentaires concernent les anciens helpers Streamlit,
ce qui explique le total de 102 réussites.

## 5. Montrer la qualité et expliquer le modèle

```powershell
ruff check .
mypy api
python -m pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
python src/courbe_seuil.py
python src/bilan_jeu_or.py
```

Attendu : ruff et mypy sans erreur ; couverture API **97,70 %**. Au seuil 0,60,
16 des 58 avis de test partent vers un humain et il reste 2 erreurs automatiques
contre 7 sans abstention. Le jeu d'or distinct donne 5 justes, 11 abstentions
et 4 erreurs franches connues : le modèle reste un prototype limité.

## 6. Faire la démonstration devant le professeur

Garder deux terminaux ouverts, chacun dans le dossier du projet et avec `.venv`
activé. Dans le premier :

```powershell
uvicorn api.main:app --reload
```

Ouvrir <http://127.0.0.1:8000/docs>. Tester `GET /health`, puis `POST /predict`
avec `{"text":"Livraison rapide, produit conforme, très satisfait"}` : 200,
`POSITIVE`, score 0,777. Avec `{"text":"   "}` : 422 et `detail` en liste.

Dans le deuxième terminal :

```powershell
streamlit run ui/app.py --server.headless true
```

Ouvrir <http://localhost:8501> et montrer successivement :

1. « Livraison rapide, produit conforme, très satisfait » : Avis positif, 78 %.
2. « Produit cassé et service injoignable, à fuir » : Avis négatif, 75 %.
3. « xqzvb wlkptr grombu » : vérification humaine, 52 %.
4. Trois espaces : avertissement de refus.
5. Onglet fichier : charger `data/avis_exemple.csv`, montrer les 6 lignes,
   le résumé 3 positifs / 2 négatifs / 1 abstention, puis télécharger le CSV.
6. Arrêter uvicorn avec Ctrl+C dans son terminal, recharger la page :
   « API injoignable ». Relancer uvicorn pour poursuivre.

Terminer en montrant [GitHub Actions](https://github.com/OthmaneW37/OthmaneMoussawi-A---AhmedRayaneRamzi-B/actions),
la dernière exécution du commit présenté, et les comptes rendus `docs/semaine2.md`
à `docs/semaine5.md`.

## Tout rejouer en une commande

```powershell
.\scripts\verifier.ps1 -Detail
```

Ce script régénère le modèle de démonstration, vérifie la qualité et exécute les
tests. Pour une capture personnelle, utiliser Windows + Maj + S avec la commande
et son résultat visibles. Les captures déjà enregistrées sont dans `docs/captures/`.
