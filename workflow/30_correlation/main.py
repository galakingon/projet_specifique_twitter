import argparse

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os.path

import seaborn as sb

parser = argparse.ArgumentParser(description =
                                 'Calcul et affiche la matrice de corrélation entre les deux clusters passés en argument.')

parser.add_argument('-r', '--cluster_ref', help = 'Clusters de référence',
                    action = 'store', default = None)

parser.add_argument('-c', '--cluster_comp', help = 'Clusters à comparer',
                    action = 'store', default = None)

parser.add_argument('-F', '--filename_out', help = 'Nom de fichier en sortie',
                        action ='store', default = None)

parser.add_argument('-n', '--number_in', help = 'Numéro associé aux deux experiences courantes en entrée',
                        action ='store', default = [0, 0],
                        type = int, nargs = 2)

parser.add_argument('-N', '--number_out', help = 'Numéro associé à l\'experience courante en sortie',
                        action ='store', default = 0, type = int)

parser.add_argument('-s', '--statistics', help = 'Indique dans un fichier en sortie des statistiques sur les valeurs de corrélation',
                        action ='store', default = None)


args = parser.parse_args()
list_valeurs = []

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

    global list_valeur
    
    for i in range(1, cluster_data1.shape[1]):
        cur_col = cluster_data1.ix[:, i]
        
        for j in range(1, cluster_data2.shape[1]):
            corr_matrix.ix[i-1, j-1] = cur_col.corr(cluster_data2.ix[:, j], method)
            list_valeurs.append(corr_matrix.ix[i-1, j-1])

    corr_matrix = corr_matrix[corr_matrix.columns].astype(float)


    return corr_matrix

# récupération des deux fichiers
# dans chacun d'eux, on a les même tweet mais
# avec des valeurs de cluster différentes

prefixe = '../../out/'

filename_base = '2x_clusters_'
ext = '.csv'


if args.cluster_ref is None:
    filename1 = filename_base + str(args.number_in[0]) + ext
else:
    filename1 = args.cluster_ref
    
if args.cluster_comp is None:
    filename2 = filename_base + str(args.number_in[1]) + ext
else:
    filename2 = args.cluster_comp

data1 = pd.read_csv(prefixe + filename1)
data2 = pd.read_csv(prefixe + filename2)

cluster_data1 = add_cluster_col(data1, 1)
cluster_data2 = add_cluster_col(data2, 2)

print("-> Do correlation...")

corr_matrix = do_corr(cluster_data1, cluster_data2)

if args.statistics is not None:

    print("-> Do statistics...")
    
    list_valeurs_supp = [valeur for valeur in list_valeurs if valeur > 0.5]
    nombre_valeurs_supp = len(list_valeurs_supp)
    
    moyenne = sum(list_valeurs) / len(list_valeurs)
    
    list_ecarts = [(moyenne - valeur)*(moyenne - valeur) for valeur in list_valeurs]
    
    ecart_types = math.sqrt(sum(list_ecarts) / len(list_ecarts))
    minimum = min(list_valeurs)
    maximum = max(list_valeurs)
    
    stats_filename = prefixe + "corr_stats_" + str(args.number_out) + ".csv"
    
    stats = pd.DataFrame(columns = ('numero_exp', 'corr_mean', 'corr_std_deviation', 'corr_min', 'corr_max', 'nombre_valeurs_supp'))
    
    stats.loc[stats.shape[1]] = [int(args.number_out), moyenne, ecart_types, minimum, maximum, nombre_valeurs_supp]
    stats.to_csv(stats_filename, index = False)
    

print("    heatmap...")

sb.heatmap(corr_matrix)

print("    ok !")

module = '30_correlation_' if args.filename_out is None else args.filename_out

plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig(prefixe + module + str(args.number_out) + '.pdf',
            format = 'pdf')
