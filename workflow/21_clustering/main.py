

# scipy.spatial.distance.cdist

# pyclust

import pandas as pd

import args

from c_dbscan import do_dbscan

# parse les arguments de la ligne de commande
args.init()


def load_data():
    # Cette fonction se charge de récupérer le fichier demandé
    # et sélectionne par défaut (sinon, TODO) tous les attributs
    # sauf l'id
    
    prefixe = '../../out/'
    filename = '1x_vecteurs_'
    
    if args.args.filename is None:
        filename += str(args.args.number) + ".csv";
    else:
        filename = args.args.filename
    
    data = pd.read_csv(prefixe + filename)
    
    # récupérer tout sauf l'id
    data = data.drop('id', axis=1)
    
    return data

data = load_data()

if args.args.method == 'dbscan':
    do_dbscan(data);

