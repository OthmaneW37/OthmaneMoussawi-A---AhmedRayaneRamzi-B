# Semaine 3 : le seuil d'incertitude

Nous retenons le seuil par défaut `SEUIL_INCERTITUDE = 0.60` : sur les 4 000 avis du jeu de test Allociné, il envoie 509 avis à un agent (12,7 %) et fait tomber les erreurs tranchées automatiquement de 318 à 126, dont les négatifs classés positifs (le cas grave, un client mécontent traité en retard) de 181 à 74.

À 0,50 aucun avis n'est vérifié et les 181 négatifs manqués passent inaperçus ; à 0,75 on n'en manque plus que 17, mais 1 626 avis (40,6 %) partent vers la file humaine, ce qui annule l'intérêt de l'automatisation pour une équipe qui reçoit des milliers d'avis par jour ; 0,60 divise par plus de deux les négatifs manqués pour une charge de relecture d'environ un avis sur huit, un compromis que nous jugeons tenable et qu'il faudrait valider avec l'équipe relation client.

Limite observée : sur nos avis e-commerce de démonstration, le modèle entraîné sur des critiques de films hésite beaucoup plus (117 avis sur 290 envoyés à un agent au même seuil, et 72,4 % de négatifs annoncés pour 50 % réels), et un avis net comme « Livraison rapide, produit conforme, je recommande. » ressort « à vérifier » à 59 % ; le seuil ne corrige pas ce changement de domaine, seules des données étiquetées du bon domaine le feraient.
