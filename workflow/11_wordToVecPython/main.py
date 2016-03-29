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

def get_tweet(nb_docs):
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
    

    label_tweet = []
    text_tweet = []
    geo_tweet = []
    userid_tweet = []
    
    i = 0
    for tweet in cursor_tweet:
        if nb_docs != 0 and i >= nb_docs:
            break
        i = i + 1

        label_tweet.append(tweet['_id'])
        text_tweet.append(tweet['text'])
        #geo_tweet.append(tweet['geo'])
        #userid_tweet.append(tweet['user']['id_str'])

    print("    " + str(len(label_tweet)) + " récupérés")
    print("    ok!")

    return label_tweet, text_tweet

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
        
        weighted_vector = None 
        
        for word in bag:
            # on calcule le tfidf
            cur_tf = float(count[word]) / bag_len
            cur_tfidf = idf[word] * cur_tf
            
            # on fait la somme pondérée des vecteurs de mot
            data[row_counter, :] += cur_tfidf * model[word]
        
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

    filename_cache = ('model_nbdocs_' + str(nb_docs) +
                          '_dim_' + str(vec_dim) +
                          '.doc2vec')
    
    if not os.path.exists(filename_cache):
    
        model = Doc2Vec(documents, size = vec_dim,
                    min_count = 1, workers = 4)
    
        model.save(filename_cache)
        
    else:
        model = Doc2Vec.load(filename_cache)
    
    
    print("   tfidf...")
    data = do_tfidf(text_tweet, model)
    
    mat_docs = np.vstack(model.docvecs)
    
    print('   mat_docs.shape = ' + str(mat_docs.shape))
    print("    ok!")
    
    model = DBSCAN(eps = 0.01, min_samples = 5)
    model.fit(mat_docs)
    
    label_doc = model.labels_
    print("doc : " + str(len(set(model.labels_))))
    print("Clustering doc ok !")
    
    return label_doc


nb_docs = 1000
vec_dim = 2

label_tweet, text_tweet = get_tweet(0)

nb_docs = len(label_tweet)

label_doc = do_doc2vec(label_tweet, text_tweet)

