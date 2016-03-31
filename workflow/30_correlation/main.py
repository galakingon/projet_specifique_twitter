import argparse

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sb

parser = argparse.ArgumentParser(description =
                                 'Calcul et affiche la matrice de corrélation entre les deux clusters passés en argument.')

parser.add_argument('clusterRef', help = 'Clustering de référence')
parser.add_argument('clusterComp', help = 'Clustering à comparer')

parser.add_argument('-f', '--filename', help = 'Nom de fichier en sortie',
                        action ='store', default = None)

parser.add_argument('-n', '--number', help = 'Numéro associé à l\'experience courante',
                        action ='store', default = 0, type = int)

args = parser.parse_args()


def add_cluster_col(data, prefix_number):
    # transformer la colonne "cluster" en plusieurs attributs
    # binaires
    
    finalData = pd.DataFrame(data['id'])
    
    val_uniques = pd.unique(data['cluster'])
    
    prefixe = 'cluster' + str(prefix_number) + "_"
    
    for value in val_uniques:
        finalData.insert(finalData.shape[1], prefixe + str(value),
            (data['cluster'] == value).astype(int))
    
    return finalData

def do_corr(cluster_data1, cluster_data2, method = 'pearson'):
    
    corr_matrix = pd.DataFrame(index = list(cluster_data1)[1:],
                               columns = list(cluster_data2)[1:])
    
    for i in range(1, cluster_data1.shape[1]):
        cur_col = cluster_data1.ix[:, i]
        
        for j in range(1, cluster_data2.shape[1]):
            corr_matrix.ix[i-1, j-1] = cur_col.corr(cluster_data2.ix[:, j], method)

    corr_matrix = corr_matrix[corr_matrix.columns].astype(float)

    return corr_matrix

# récupération des deux fichiers
# dans chacun d'eux, on a les même tweet mais
# avec des valeurs de cluster différentes

prefixe = '../../out/'

data1 = pd.read_csv(prefixe + args.clusterRef)
data2 = pd.read_csv(prefixe + args.clusterComp)

cluster_data1 = add_cluster_col(data1, 1)
cluster_data2 = add_cluster_col(data2, 2)

corr_matrix = do_corr(cluster_data1, cluster_data2)

print(corr_matrix)

sb.heatmap(corr_matrix)

module = '30_correlation_' if args.filename is None else args.filename

plt.savefig(prefixe + module + str(args.number) + '.pdf', format = 'pdf')
