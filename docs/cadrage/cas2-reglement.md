# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Permettre à un salarié de poser une question en langage courant sur le règlement intérieur et d'obtenir une réponse qui cite l'article exact sur lequel elle s'appuie.

## Utilisateur final (obligatoire)

Les salariés de l'entreprise, et en second lieu l'équipe RH qui reçoit aujourd'hui ces questions par courriel.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

La réponse existe déjà dans un document : il faut la retrouver et la citer, pas l'inventer. (b) La vérifiabilité est le critère décisif : le salarié et les RH doivent pouvoir relire l'article cité, ce que le RAG permet en renvoyant le passage source. (a) Il n'existe aucun jeu de questions-réponses étiquetées, donc le machine learning supervisé est exclu. (c) Le volume est faible, quelques dizaines de questions par jour, donc le coût par requête d'un modèle de langage reste acceptable. (d) Une mauvaise réponse peut induire un salarié en erreur sur ses droits, d'où l'obligation de citer la source.

## Données nécessaires et leur origine (obligatoire)

Le règlement intérieur dans sa version en vigueur, découpé par article, ainsi que les notes de service qui le complètent ; fournis par la direction des ressources humaines et mis à jour à chaque révision.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur 50 questions de référence rédigées avec les RH, au moins 90 % de réponses citant le bon article, et 100 % de réponses comportant une citation ou un « je ne sais pas » explicite.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse erronée peut conduire un salarié à une décision contraire au règlement (congés, horaires, sanctions). Chaque réponse affiche l'article cité et un lien vers les RH ; les questions sans source trouvée sont transmises à un agent RH.

## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler des situations personnelles (santé, conflit, sanction) : pas de conservation nominative des questions, et un modèle hébergé dans un cadre conforme au RGPD.

## Approche écartée et pourquoi (facultatif)

Le modèle génératif seul a été écarté : sans le document, il répond avec des règles génériques ou inventées, et ne peut citer aucun article.
