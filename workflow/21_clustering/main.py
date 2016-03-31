

# scipy.spatial.distance.cdist

# pyclust

import pandas as pd

import args

from c_dbscan import do_dbscan

# parse les arguments de la ligne de commande
args.init()


def load_data():
    
    prefixe = '../../out/'
    filename = '1x_vecteurs_'
    
    if args.args.filename is None:
        filename += str(args.args.number) + ".csv";
    
    data = pd.read_csv(prefixe + filename)
    
    return data


data = load_data()

if args.args.method == 'dbscan':
    do_dbscan(data);

