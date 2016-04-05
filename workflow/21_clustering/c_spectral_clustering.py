import args

from sklearn import cluster
import numpy as np
import scipy.spatial.distance as sp_d

def get_matrice_distance(data, distance):
    return sp_d.squareform(sp_d.pdist(data.as_matrix(), metric = distance))

def get_matrice_similarite(matrice_distance, delta = 1):
    return np.exp(- matrice_distance ** 2 / (2. * delta ** 2))

def do_spectral_clustering(data):
    
    print("-> Do spectral clustering...")
    
    # récupération des paramètres
    
    nb_clusters = int(args.associer_param('clusters', 2))
    delta = args.associer_param('delta', 1)
    
    print("    compute similarity...")
    
    matrice_dist = get_matrice_distance(data,
                                        args.args.distance)
    
    matrice_sim = get_matrice_similarite(matrice_dist,
                                         delta = delta)
    
    print("    cluster...")
    
    model = cluster.SpectralClustering(affinity = 'precomputed',
                                       n_clusters = nb_clusters)
    
    
    
    labels = model.fit_predict(matrice_sim)
    
    data['cluster'] = labels
    
    print("    ok !")
    
    return data