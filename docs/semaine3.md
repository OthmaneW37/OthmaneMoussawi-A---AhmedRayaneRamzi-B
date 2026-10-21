# Semaine 3 : exposer le modèle par une API

Vérifications refaites le 21 octobre 2026 avec le modèle de démonstration : les six tests du kit API passent. Les essais HTTP réels donnent `/health` en 200, un avis positif à 0,777 et un négatif à 0,7465. Les corps vides, sans champ `text` ou avec un nombre sont refusés en 422. Les réponses des essais sont dans [essais-http.json](verification/essais-http.json).

## 1. Pourquoi refuser de démarrer sans modèle ?

Le contexte de démarrage charge `models/sentiment.joblib` avant de servir la première requête. Le test `test_modele_absent_refuse_demarrage` redirige ce chemin vers un fichier absent, vide le cache et observe un `FileNotFoundError` à l'ouverture de `TestClient`. Une instance sans modèle n'est donc jamais annoncée prête. Le 503 garde un autre rôle : signaler un modèle retiré ou indisponible après le démarrage ; nous vérifions ce cas sur `/health` et `/predict`.

## 2. Le double refus d'un texte vide est-il redondant ?

Les deux contrôles protègent deux points d'entrée : Pydantic valide le contrat HTTP, tandis que `predict()` peut être appelée directement depuis Python ou le terminal. Au départ du kit, les espaces passaient le schéma puis donnaient un 422 avec un `detail` sous forme de chaîne. Le TP4 ajoute le même contrôle `str.strip()` au schéma : tous les blancs, y compris U+0085, sont maintenant refusés avant le modèle, dans la liste standard d'erreurs Pydantic. Une `ValueError` venant ensuite du modèle est une panne interne et reçoit 500, sans divulguer son message.

![Santé de l'API réellement démarrée](captures/tp3-t15-health.png)
