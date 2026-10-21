# Semaine 2 : analyse des erreurs du modèle

Sur le jeu de démonstration, le modèle commet 7 erreurs sur 58 avis de test (F1 macro 0,879) : 2 avis négatifs classés positifs et 5 positifs classés négatifs, et les 7 sont des avis mitigés, par exemple « Service impeccable et livraison en avance sur le papier, sauf que ensuite produit cassé à l'arrivée. », étiqueté négatif mais prédit positif avec une confiance de 0,56.

Ces erreurs viennent de la représentation en sac de mots (TF-IDF) : elle compte les mots positifs et négatifs mais ignore leur ordre, si bien que « bon puis mauvais » et « mauvais puis bon » donnent presque le même vecteur, alors que l'étiquette dépend de la seconde moitié de la phrase, celle qui conclut ; le modèle le « sait » d'ailleurs à moitié, puisque ses confiances sur ces 7 erreurs restent entre 0,53 et 0,69.

Pour les corriger, il faudrait une représentation qui tienne compte de l'ordre et du contexte, comme des embeddings de phrase ou un modèle de type transformeur (semaine 9), ou à défaut davantage d'avis mitigés étiquetés ; en attendant, un seuil d'incertitude qui renvoie ces avis peu sûrs à un agent limite les dégâts.

## Nouvelle exécution du 21 octobre 2026

Les quatre scripts du TP2 correspondent au kit de rattrapage (hors typage ajouté au TP4 et corrections de qualité dans l'évaluation). Le jeu de démonstration a été régénéré : 290 avis, 232 pour l'entraînement et 58 pour le test, vocabulaire de 316 termes, F1 macro 0,879 et matrice `[[27, 2], [5, 24]]`.

L'expérience Allociné a également été refaite : 20 000 avis, 16 000 pour l'entraînement et 4 000 pour le test, F1 macro et exactitude 0,9205, rappel négatif 0,9113. Les [métriques de cette nouvelle exécution](verification/metrics-allocine.json) sont conservées. Le modèle actif et `models/metrics.json` ont ensuite été reconstruits sur le jeu de démonstration, conformément au guide pour les tests API et interface. Ces scores portent sur des jeux et domaines différents : leur différence ne prouve pas à elle seule qu'un modèle est meilleur pour le service client.
