import argparse

args = None

def init():
    global args
    
    parser = argparse.ArgumentParser(description =
                                     'Cluster la collection de tweet passé en paramètre')
    
    # par défaut, cluster sur tout sauf l'id
    
    parser.add_argument('filename',
                        help = 'Fichier contenant la collection des vecteurs de tweet')
    
    parser.add_argument('-m', '--method', help = 'Méthode de clustering',
                        action = 'store', choices = ['dbscan'],
                        default = None)
    
    args = parser.parse_args()