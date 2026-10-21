# Semaine 4 : tests approfondis et qualité

Mesures du 21 octobre 2026, Python 3.11.9, modèle de démonstration réentraîné. Les sorties avant correction viennent d'une copie temporaire du code API original du kit, exécutée avec le même environnement et le même modèle. Les tests complétés sont exécutés sur cette copie puis sur le code corrigé ; aucun seuil de test fourni n'a été abaissé.

## 1. Couverture avant et après

Avant : **91 %**, 69 instructions dont 6 non couvertes. Dans `api/main.py`, la ligne 49 correspondait au 503 sans modèle, les lignes 77–79 à la journalisation et au 500, et les lignes 85–87 au lancement direct avec uvicorn. Les six tests du TP3 ne provoquaient pas ces pannes. [Sortie initiale](verification/couverture-avant.txt).

Après : **97,70 %**, 87 instructions dont 2 non couvertes, toutes dans le bloc de lancement direct `if __name__ == "__main__"`. Le démarrage habituel se fait avec `uvicorn api.main:app`, et `TestClient` exécute le lifespan. Aucune ligne n'est exclue de la mesure, aucun `pragma: no cover` n'est ajouté. [Résultat complet](verification/tests-et-couverture.txt).

## 2. Défauts mis en évidence

La suite complétée appliquée au kit initial donne **5 failed, 13 passed**. [Échecs avant correction](verification/defauts-avant.txt).

| Symptôme | Test révélateur | Correction |
| --- | --- | --- |
| Espaces : `detail` est une chaîne | `test_frontieres_du_contrat[espaces]` | `field_validator` dans le schéma |
| U+0085 et autres blancs Unicode : refus non uniforme | cas explicite `blanc-unicode` et propriété `test_tout_texte_blanc_refuse` | Même règle `str.strip()` que le TP2 |
| `ValueError("bug interne")` devient 422 et expose son message | `test_panne_modele_repond_500_sans_detail_interne[erreur1]` | Toute panne de prédiction devient 500 générique, journalisée côté serveur |
| Modèle contenant une classe inconnue accepté au démarrage | `test_classes_inconnues_refusees` | Comparaison des classes avec la correspondance explicite au démarrage |

Les autres tests d'intégration couvrent le démarrage réel, l'absence du fichier avec cache vidé, le 503 sur les deux routes et la panne `RuntimeError`. Le seuil est testé à 0,5999, 0,60 et 0,6001 ; le texte de réponse est limité à 100 caractères. Les propriétés Hypothesis passent sur plusieurs exécutions successives, dont trois dans la suite globale et sa vérification détaillée.

## 3. Seuil d'abstention

Mesure sur les mêmes 58 avis de test, jamais utilisés pour ajuster le vectoriseur :

| Seuil | Réponses automatiques | Exactitude de ces réponses | Erreurs automatiques | Vers un humain |
| --- | --- | --- | --- | --- |
| 0,50 | 58 / 58 | 0,879 | 7 | 0 |
| 0,60 | 42 / 58 | 0,952 | 2 | 16 |
| 0,70 | 37 / 58 | 1,000 | 0 | 21 |

Nous retenons `SEUIL_ABSTENTION = 0.60` : 27,6 % de relecture, cinq erreurs automatiques évitées sur sept. Monter à 0,70 évite les deux dernières erreurs sur ce petit jeu, mais impose cinq relectures de plus. Ce choix reste à valider sur des avis représentatifs ; le score n'est pas une probabilité de correction garantie. Un texte inconnu donne `INDETERMINE` à 0,5162 : sans mot du vocabulaire, son vecteur TF-IDF est nul et la régression ne conserve que son biais. [Courbe complète](verification/courbe-seuil.txt).

## 4. Jeu d'or

20 avis originaux proposés pour relecture par le binôme, dont 10 difficiles (négation, ironie, avis mitigés, autres domaines), sans doublon dans les 290 avis de démonstration. **5 justes, 11 abstentions, 4 erreurs franches déclarées** ; le test donne **17 passed, 4 xfailed**. [Bilan détaillé](verification/bilan-jeu-or.txt).

Les quatre erreurs restent dans le fichier : résolution d'un problème mal reconnue, dégâts d'emballage, négation « ni…ni », et avis de restauration. Les raisons sont des interprétations des limites du sac de mots ; les étiquettes attendues et les textes n'ont pas été adaptés pour améliorer le résultat. `xfail(strict=True)` signalera aussi une correction future inattendue. Le petit modèle laisse donc encore passer de vraies erreurs, même au-dessus du seuil. La [relecture assistée des vingt étiquettes](relecture-jeu-or.md) a été réalisée à la demande du binôme, sans changer les textes ni les résultats. La rédaction et la validation personnelles demandées par l'enseignant restent distinctes de cette vérification technique.

## 5. Outils statiques et automatisation

Avant : **17 remarques ruff**, dont 11 sur le code fourni, 3 sur les anciens helpers et 3 d'ordre des imports dans les tests complétés ; **0 erreur mypy**. [Ruff initial](verification/ruff-avant.txt), [mypy initial](verification/mypy-avant.txt).

Après : ruff affiche `All checks passed!` et mypy `Success: no issues found in 4 source files`. Les imports sont rangés, les noms `l` deviennent `ligne`, les `zip()` d'évaluation utilisent `strict=True`, et le 500 utilise `from None`. Les seuls changements aux assertions des anciens tests sont inexistants : leurs renommages de variables ne changent pas les vérifications. Le contrat de retour utilise maintenant des `TypedDict` et des étiquettes `Literal`, avec une correspondance explicite au lieu de `.upper()`.

Aucun des quatre défauts de comportement du tableau n'était détecté par ruff ou mypy au départ. Les outils détectent des constructions risquées et des incohérences de types ; les tests exécutés restent nécessaires. Le hook local lance ruff et mypy, et la CI entraîne le modèle avant de contrôler qualité, tests et couverture minimale de 95 %. Le résultat du contrôle de refus du hook est enregistré dans le journal.
