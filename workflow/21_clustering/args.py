import argparse
import scipy.spatial.distance as sp_d


args = None
dict_distances = None
dict_parametres = None

def get_parametres(liste):
    # Construit un dictionnaire à partir d'une liste où chaque élément
    # est de la forme parametre=valeur
    
    return {key:float(val) for key, val in 
            (element.split('=') for element in liste)
            }

def init():
    # Récupère les arguments de la ligne de commande
    # et s'occupe d'initialiser différentes variables globales.
    
    
    # Initialisation du dictionnaire de correspondance
    # chaîne de caractère <=> fonction de distance
    
    global dict_distances
    
    dict_distances = {'euclidienne' : sp_d.euclidean,
                     'manhattan' : sp_d.cityblock,
                     'cosine' : sp_d.cosine,
                     'hamming' : sp_d.hamming}
    
    # Traitement des arguments provenant de la ligne de commande
    
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
    
    parser.add_argument('-d', '--distance', help = 'Distance utilisée',
                        action = 'store',
                        choices = dict_distances.keys())
    
    parser.add_argument('-p', '--parameters', help = 'Liste des paramètres associés à l\'algorithme choisi via --method',
                        action = 'store', nargs = '*', default = [])
    
    parser.add_argument('-o', '--output', help = 'Nom de fichier en sortie',
                        action ='store', default = None)

    parser.add_argument('-n', '--number', help = 'Numéro associé à l\'experience courante',
                        action ='store', default = 0, type = int)
    
    args = parser.parse_args()
    
    global dict_parametres

    if args.parameters is None:
        dict_parametres = {}
    else:
        dict_parametres = get_parametres(args.parameters)
    
    print (dict_parametres)
       
       
def associer_param(param, param_default = 0):
    
    if param in dict_parametres:
        return dict_parametres[param]
    else:
        return param_default
    
    
    