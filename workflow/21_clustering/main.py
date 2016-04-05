

# scipy.spatial.distance.cdist

# pyclust

import pandas as pd

import args

from c_dbscan import do_dbscan
from c_spectral_clustering import do_spectral_clustering

# parse les arguments de la ligne de commande
args.init()

colonne_id = None

def load_data():
    # Cette fonction se charge de récupérer le fichier demandé
    # et sélectionne par défaut (sinon, TODO) tous les attributs
    # sauf l'id
    
    global colonne_id
    
    prefixe = '../../out/'
    filename = '1x_vecteurs_'
    
    if args.args.filename_in is None:
        filename += str(args.args.number_in) + ".csv";
    else:
        filename = args.args.filename_in
    
    data = pd.read_csv(prefixe + filename)
    
    colonne_id = data['id']
    
    # récupérer tout sauf l'id
    data = data.drop('id', axis=1)
    
    return data

data = load_data()
final_data = None

if args.args.method == 'dbscan':
    final_data = do_dbscan(data)
elif args.args.method == 'spectral_clustering':
    final_data = do_spectral_clustering(data)

final_data['id'] = colonne_id


# sauvegarder le fichier

prefix = '../../out/'

if args.args.filename_out is not None:
    nom = args.args.filename_out
    ext = '.csv'
    
    if args.args.filename_out[-4:] == '.csv':
        nom = args.args.filename_out[:-4]
        
    final_data.to_csv(prefix + nom + '_' + str(args.args.number_out) + ext, index = False)
else:
    final_data.to_csv(prefix + '2x_clusters_' + str(args.args.number_out) + '.csv',
                index = False)

