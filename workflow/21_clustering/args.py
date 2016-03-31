import argparse

args = None

def init():
    global args
    
    parser = argparse.ArgumentParser(description =
                                     'Cluster la collection de tweet passé en paramètre')
    
    # par défaut, cluster sur tout sauf l'id
    
    parser.add_argument('-f', '--filename',
                        help = 'Fichier contenant la collection des vecteurs de tweet',
                        action = 'store', default = None)
    
    parser.add_argument('-m', '--method', help = 'Méthode de clustering',
                        action = 'store', choices = ['dbscan'],
                        required = True)
    
    parser.add_argument('-o', '--output', help = 'Nom de fichier en sortie',
                        action ='store', default = None)

    parser.add_argument('-n', '--number', help = 'Numéro associé à l\'experience courante',
                        action ='store', default = 0, type = int)
    
    args = parser.parse_args()
    