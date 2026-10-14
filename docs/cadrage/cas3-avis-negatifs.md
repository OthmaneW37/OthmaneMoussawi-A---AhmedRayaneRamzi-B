# Fiche de cadrage : Avis clients négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Faire remonter automatiquement les avis clients négatifs en tête de la file de traitement, au lieu de les traiter dans l'ordre d'arrivée.

## Utilisateur final (obligatoire)

Les agents de l'équipe relation client, qui traitent plusieurs milliers d'avis par jour et doivent répondre en priorité aux clients mécontents.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Il n'existe pas de logique simple et stable pour reconnaître un avis négatif : une liste de mots-clés échoue dès qu'apparaissent ironie, négation ou retournement. (a) Les données étiquetées sont gratuites : la note en étoiles laissée avec chaque avis fournit l'étiquette. (c) Le volume, des milliers d'avis par jour, impose un coût par requête très faible, ce qu'un classifieur léger offre et qu'un modèle génératif n'offre pas. (d) Une erreur est peu grave : un avis mal classé est traité un peu plus tard, pas perdu.

## Données nécessaires et leur origine (obligatoire)

L'historique des avis clients avec leur note, la note servant d'étiquette (1-2 étoiles négatif, 4-5 positif) ; pour le prototype, le jeu public Allociné de 20 000 critiques étiquetées.

## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro d'au moins 0,85 sur un jeu de test jamais vu à l'entraînement, avec une attention particulière au rappel sur la classe négative, qui mesure les clients mécontents effectivement remontés.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un faux négatif (avis négatif classé positif) fait attendre un client mécontent ; un faux positif fait traiter trop tôt un avis sans urgence. Les avis dont la confiance est faible sont envoyés à un agent pour vérification.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms, adresses ou numéros de commande : pseudonymisation avant entraînement, et vigilance sur les biais du modèle envers certaines formulations ou registres de langue.

## Approche écartée et pourquoi (facultatif)

Les règles métier par mots-clés ont été écartées, car elles ne gèrent pas les négations et les retournements (« bien emballé, mais cassé à l'arrivée »).
