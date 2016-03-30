from pymongo import MongoClient

from matplotlib import pyplot as plt

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from sklearn.cluster import DBSCAN

import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import os

from collections import Counter
import math
import argparse

# Traitement de la ligne de commande

parser = argparse.ArgumentParser(description =
                                 'Exécute Doc2Vec sur la base de Tweet')


exc_group = parser.add_mutually_exclusive_group()
exc_group.add_argument('-m', '--mean', help = 'Moyenne les vecteurs de mots',
                       action = 'store_true')
exc_group.add_argument('-s', '--sum', help = 'Somme les vecteurs de mots',
                       action = 'store_true')
exc_group.add_argument('-t', '--tfidf', help = 'Effectue la somme pondérée (tfidf) des vecteurs de mots',
                       action = 'store_true')

parser.add_argument('-d', '--dim', help = 'Dimension des vecteurs de mots',
                        action ='store', default = 2, type = int)

parser.add_argument('-c', '--coeff', help = 'Associe un coefficient aux hashtags',
                        action ='store', default = 1, type = int)

parser.add_argument('-a', '--amount', help = 'Nombre de tweet à considérer (0 prend toute la base)',
                        action ='store', default = 0, type = int)

parser.add_argument('-f', '--filename', help = 'Nom de fichier en sortie',
                        action ='store', default = None)

parser.add_argument('-n', '--number', help = 'Numéro associé à l\'experience courante',
                        action ='store', default = 0, type = int)


args = parser.parse_args()

def get_tweet():
    print("-> Récupération des tweets...")
    client = MongoClient()
    
    col_twitter = client.projet_specifique.tweets
    #tweet géolocalisés
    if False:
        cursor_tweet = col_twitter.find({"geo":{"$ne":None}},
                                    {'text':1, '_id':1,
                                    "geo":1, "user.id_str":1})
    else:
        cursor_tweet = col_twitter.find({},{'text':1, '_id':1})
    
    if args.amount > 0:
        cursor_tweet.limit(args.amount)

    label_tweet = []
    text_tweet = []
    
    i = 0
    for tweet in cursor_tweet:
        i = i + 1

        label_tweet.append(tweet['_id'])
        text_tweet.append(tweet['text'])
        #geo_tweet.append(tweet['geo'])
        #userid_tweet.append(tweet['user']['id_str'])

    print("    " + str(len(label_tweet)) + " récupérés")
    print("    ok!")

    return label_tweet, text_tweet

def is_hashtag(word):
    return True if word[0] == '#' else False

def do_tfidf(text_tweet, model):
    # text_tweet est une collection de documents
    # model est le modèle Doc2Vec entraîné
    
    # création du vocabulaire
    
    _vocab = []
    tweet_word = {}
    
    for tweet in text_tweet:
        tweet_word.update({tweet : tweet.split()})
        _vocab.extend(tweet_word[tweet])
    
    # unicité
    vocab = set(_vocab)
    
    # idf
    
    idf = {}
    nb_tweet = len(text_tweet)
    
    for word in vocab:
        counter = 0
        
        for tweet in text_tweet:
            if word in tweet_word[tweet]:
                counter += 1
        
        cur_idf = math.log(float(nb_tweet) / counter)
        idf.update({word:cur_idf})
    
    # tfidf + combinaison   
    print("   combiner les vecteurs...")

    vector_dim = model.syn0.shape[1]
        
    data = np.zeros((nb_tweet, vec_dim))

    row_counter = 0
    
    for tweet in text_tweet:
                
        bag = tweet.split()
        bag_len = len(bag)
        
        count = Counter(bag) 
        
        for word in bag:
            # on calcule le tfidf
            cur_tf = float(count[word]) / bag_len
            cur_tfidf = idf[word] * cur_tf
            cur_pond = 1
            
            if is_hashtag(word):
                cur_pond = args.coeff
            
            # on fait la somme pondérée des vecteurs de mot
            data[row_counter, :] += cur_tfidf * model[word]
        
        row_counter += 1
    
    return data

def do_mean(text_tweet, model, mean = False):
    
    vector_dim = model.syn0.shape[1]
    nb_tweet = len(text_tweet)
    
    data = np.zeros((nb_tweet, vector_dim))
    
    row_counter = 0
    
    for tweet in text_tweet:
        
        bag = tweet.split()
        sum_pond = 0
        
        for word in bag:
            cur_pond = 1
            
            if is_hashtag(word):
                cur_pond = args.coeff
            
            if mean:
                sum_pond += cur_pond
            
            # on fait la somme pondérée des vecteurs de mot
            data[row_counter, :] += model[word] * cur_pond
        
        if mean:
            # on divise par la pondération
            data[row_counter, :] /= float(sum_pond)
        
        row_counter += 1
    
    return data

def do_doc2vec(label_tweet, text_tweet):

    # Traitement : exécute Doc2Vec sur l'ensemble des
    # tweets étiquetés passés en paramètre.

    # Retourne : la matrice des vecteurs lignes associés à chaque
    # tweet.
    
    print("-> Doc2Vec...")
    
    documents = [TaggedDocument(words = text.split(),
                             tags = [label]) for (label, text) in zip(label_tweet, text_tweet)]

    model = None

    filename_cache = ('model_nbdocs_' + str(args.amount) +
                          '_dim_' + str(args.dim) +
                          '.doc2vec')
    
    if not os.path.exists(filename_cache):
    
        model = Doc2Vec(documents, size = args.dim,
                    min_count = 1, workers = 4)
    
        model.save(filename_cache)
        
    else:
        model = Doc2Vec.load(filename_cache)
    
    data = None
    
    if args.coeff != 1:
        print("    pondération des #tags : " + str(args.coeff))
    
    if args.tfidf:
        print("    tfidf...")
        data = do_tfidf(text_tweet, model)
    elif args.mean:
        print("    mean...")
        data = do_mean(text_tweet, model, True)
    else:
        print("    sum...")
        data = do_mean(text_tweet, model)
    
    
    print("    ok!")
    
    # rassembler les labels de chaque tweet
    # avec les vecteurs correspondants
    
    data = pd.DataFrame(data)
    
    final_data = pd.DataFrame({'id' : label_tweet})
    final_data = pd.concat([final_data, data], axis = 1)
    
    return final_data


label_tweet, text_tweet = get_tweet()
data = do_doc2vec(label_tweet, text_tweet)

# sauvegarder le fichier

prefix = '../../out/'

if args.filename is not None:
    nom = args.filename
    ext = '.csv'
    
    if args.filename[-4:] == '.csv':
        nom = args.filename[:-4]
        
    data.to_csv(prefix + nom + '_' + str(args.number) + ext)
else:
    data.to_csv(prefix + '1x_vecteurs_python_' + str(args.number) + '.csv')
