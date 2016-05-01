import subprocess as subp

nb_tweet = 2000
nb_dim = 10

fichierVec = '1'

fichier1 = '1'
fichier2 = '2'

fichierCorr = '1'

nb_clusters = 20
eps = 0.5
min_points = 5

subp.call('python ../11_wordToVecPython/main.py' +
     ' -a ' + str(nb_tweet) + ' -d ' + str(nb_dim) + ' -n ' + fichierVec)

distance1 = 'euclidean'
distance2 = 'cosine'

subp.call('python ../21_clustering/main.py' +
     ' -n ' + fichierVec + ' -m spectral_clustering' +
     ' -d ' + distance1 +
     ' -N ' + fichier1 + ' -p clusters=' + str(nb_clusters))
  
subp.call('python ../21_clustering/main.py' +
     ' -n ' + fichierVec + ' -m spectral_clustering' +
     ' -d ' + distance2 +
     ' -N ' + fichier2 + ' -p clusters=' + str(nb_clusters))

subp.call('python ../30_correlation/main.py' +
     ' -n ' + fichier1 + ' ' + fichier2 +
     ' -N ' + fichierCorr)

fichier3 = '3'
fichier4 = '4'
 
subp.call('python ../21_clustering/main.py' +
     ' -n ' + fichierVec + ' -m dbscan' +
     ' -d ' + distance1 +
     ' -N ' + fichier3 + ' -p eps=' + str(eps) +
     ' min_pts=' + str(min_points))
 
subp.call('python ../21_clustering/main.py' +
     ' -n ' + fichierVec + ' -m dbscan' +
     ' -d ' + distance1 + 
     ' -N ' + fichier4 + ' -p eps=' + str(eps) +
     ' min_pts=' + str(min_points+5))
  
subp.call('python ../30_correlation/main.py' +
     ' -n ' + fichier1 + ' ' + fichier3 +
     ' -N 2')
 
subp.call('python ../30_correlation/main.py' +
     ' -n ' + fichier1 + ' ' + fichier4 +
     ' -N 3')
