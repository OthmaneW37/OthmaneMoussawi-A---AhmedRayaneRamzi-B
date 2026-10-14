# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Signaler au pharmacien, au moment de la saisie, toute ordonnance à laquelle il manque une mention obligatoire (prescripteur, date, posologie, durée, signature) avant la délivrance.

## Utilisateur final (obligatoire)

Le pharmacien et le préparateur au comptoir, qui saisissent l'ordonnance dans le logiciel d'officine et décident de délivrer ou non.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

La liste des mentions obligatoires est fixée par la réglementation : la logique est connue et stable, il n'y a rien à apprendre. (a) Il n'existe pas d'historique d'ordonnances étiquetées « complète / incomplète » ; il faudrait le constituer, alors que les règles s'écrivent directement. (b) Chaque alerte doit dire quelle mention manque, ce qu'une règle explicite fait naturellement et qu'un modèle statistique ne garantit pas. (d) Une ordonnance incomplète délivrée peut mettre un patient en danger : on veut un comportement déterministe et auditable. (c) Une règle coûte quasiment zéro par requête.

## Données nécessaires et leur origine (obligatoire)

Les champs saisis de l'ordonnance (prescripteur, numéro RPPS, date, médicaments, posologie, durée) dans le logiciel d'officine, et la liste réglementaire des mentions obligatoires, y compris les règles propres aux stupéfiants et aux médicaments d'exception.

## Métrique de succès et seuil d'acceptation (obligatoire)

Rappel de 100 % sur un jeu de 200 ordonnances de test construites à la main (aucune ordonnance incomplète ne passe), et moins de 5 % de fausses alertes pour ne pas lasser le pharmacien.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une ordonnance incomplète non signalée peut conduire à une délivrance erronée, donc à un risque pour le patient et à une faute professionnelle. L'outil ne bloque rien : il alerte, et c'est le pharmacien qui valide la délivrance ou contacte le prescripteur.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances sont des données de santé, soumises au RGPD et au secret professionnel : traitement local, sans envoi à un service externe, et journal des alertes accessible au seul personnel de l'officine.

## Approche écartée et pourquoi (facultatif)

Un modèle génératif lisant l'ordonnance a été écarté : il peut affirmer qu'une mention est présente alors qu'elle ne l'est pas, sans pouvoir le prouver, ce qui est inacceptable vu (d).
