# Clustering des données

fuzzy c means (k means à base de logique flou, les vecteurs ne sont plus dans un cluster mais dans plusieurs à la fois avec une probabilité différente) 

Rscript fuzzy_words_clouds.R vecteurs_java_tfidf.csv 15 10000 (le module d'évaluation du nombre de clusters nous a donné environs 15 clusters pour ces 10000 tweets) 

sorties : 

un words cloud pour chaque cluster

bientôt : les probabilités d'affectation de chaque vecteurs (permettant peut être de remonter aux topics via les clouds, à voir ... )
