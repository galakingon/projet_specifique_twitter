import subprocess as subp
import pandas as pd
import os.path

nb_tweet = 2000
nb_dim = 10

fichierVec = '1'

fichier1 = '1'
fichier2 = '2'

fichierCorr = '1'

nb_clusters = 20
eps = 1
min_points = 5

pond_hashtag = '10'
params_aggregation = ['-m', '-s', '-t', '-m -c ' + pond_hashtag, '-s -c ' + pond_hashtag, '-t -c ' + pond_hashtag]
numero_exp = 1

for param in params_aggregation:
    subp.call('python ../11_wordToVecPython/main.py ' + param + 
              ' -a ' + str(nb_tweet) + ' -d ' + str(nb_dim) + ' -n ' + str(numero_exp))
    numero_exp += 1
    
distance = 'euclidean'

for numero in range(len(params_aggregation)):
    subp.call('python ../21_clustering/main.py' +
              ' -n ' + str(numero + 1) + ' -m spectral_clustering' +
              ' -d ' + distance +
              ' -N ' + str(numero + 1) + ' -p clusters=' + str(nb_clusters))

for numero1 in range(len(params_aggregation)):
    for numero2 in range(numero1 + 1, len(params_aggregation)):
        
        subp.call('python ../30_correlation/main.py' +
                  ' -n ' + str(numero1 + 1) + ' ' + str(numero2 + 1) +
                  ' -N ' + str(numero1 + 1) + str(numero2 + 1) +
                  ' -s 1')


prefixe = '../../out/corr_stats_'
ext = '.csv'

data = None

for numero1 in range(len(params_aggregation)):
    for numero2 in range(numero1 + 1, len(params_aggregation)):
        
        stats_filename = prefixe + str(numero1 + 1) + str(numero2 + 1) + ".csv"
        
        if os.path.isfile(stats_filename):
            if data is None:
                data = pd.read_csv(stats_filename)
            else:
                data_supp = pd.read_csv(stats_filename)
                data = pd.concat([data, data_supp])

data.to_csv(prefixe + "final.csv", index = False)