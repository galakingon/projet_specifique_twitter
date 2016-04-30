import args

from sklearn import cluster

def do_dbscan(data):
    
    print(" Do dbscan...")
    
    # Récupération des paramètres
    
    eps = args.associer_param('eps', 1)
    min_pts = args.associer_param('min_pts', 1)
    
    model = cluster.DBSCAN(eps = eps,
                           min_samples = min_pts,
                           metric = args.dict_distances[args.args.distance])
    
    labels = model.fit_predict(data)
    
    data['cluster'] = labels
    
    print("   ok !")
    
    return data
