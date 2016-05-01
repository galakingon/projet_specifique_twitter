
def get_fichier(filename_prefix, filename_arg, number_arg):
    # Fonction renvoyant le nom du fichier demandé bien formé
    
    filename = ''
    number = ''
    ext = '.csv'
    
    if filename_arg is None:
        #
        if number_arg is not None:
            number = str(number_arg)
            
        filename = filename_prefix + number + ext
    else:
        filename = filename_arg
        
    return filename
    