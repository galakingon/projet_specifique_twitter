# best number of clusters evaluation for some algorithms 

Yet implementing : 
kmeans : akaike information criterion, bayesian information criterion, elbow method 
DBscan : number of cluster function of eps, 

to be implementing soon :
DBscan : better indicators
hierarchical clustering

args[1] : filename in out folder
args[2] : number of points that should be used (no default value yet so please specify a number) 

output : 
in out folder : <filename without extension _nb_clusters>/<algorithm name>/graphs_for_all_the_methods_used.jpg

Rscript clustering_tweets.R vecteurs_java_tfidf.csv 1000

output :

vecteurs_java_tfidf_nb_clusters/kmeans/vecteurs_java_tfidf_elbow.jpg
vecteurs_java_tfidf_nb_clusters/kmeans/vecteurs_java_tfidf_aic.jpg
vecteurs_java_tfidf_nb_clusters/kmeans/vecteurs_java_tfidf_bic.jpg
vecteurs_java_tfidf_nb_clusters/DBscan/vecteurs_java_tfidf_eps.jpg
