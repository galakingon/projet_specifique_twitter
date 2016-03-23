from pymongo import MongoClient

from matplotlib import pyplot as plt

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from sklearn.cluster import DBSCAN

import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import os

def get_tweet(nb_docs):
    print("-> Récupération des tweets...")
    client = MongoClient()
    
    col_twitter = client.twitter.twitter
    #tweet géolocalisés
    cursor_tweet = col_twitter.find({"geo":{"$ne":None}},
                                    {'text':1, '_id':1,
                                    "geo":1, "user.id_str":1})

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
        geo_tweet.append(tweet['geo'])
        userid_tweet.append(tweet['user']['id_str'])

    print("    " + str(len(label_tweet)) + " récupérés")
    print("    ok!")

    return label_tweet, text_tweet, geo_tweet, userid_tweet

def get_dendrogram(data,
                   method = 'single',
                   show = False):
    
    # Traitement : calcule le dendrogramme associé à la
    # classification hiérarchique du jeu de données passé
    # en paramètre.
    # Si show est vrai, le dendrogramme est affiché, sinon
    # il est sauvegardé sur le disque (par défaut).

    linkage_matrix = sch.linkage(data,
                                 method = method)
    
    plt.figure(figsize = (25, 10))
    plt.title('Clustering Ascendant Hiérarchique (' + method + ')')
    plt.xlabel('tweets')
    plt.ylabel('distance euclidienne')
    sch.dendrogram(
        linkage_matrix,
        leaf_rotation = 90.,
        leaf_font_size = 8.
        )
    
    plt.savefig('plot_nbdocs_' + str(nb_docs) +
                '_dim_' + str(vec_dim) +
                '_cah_' + method + '.png')
    if show:
        plt.show()


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
                    min_count = 1, workers = 2)
    
        model.save(filename_cache)
        
    else:
        model = Doc2Vec.load(filename_cache)
    
    mat_docs = np.vstack(model.docvecs)
    
    print('   mat_docs.shape = ' + str(mat_docs.shape))
    print("    ok!")
    
    model = DBSCAN(eps = 0.01, min_samples = 5)
    model.fit(mat_docs)
    
    label_doc = model.labels_
    print("doc : " + str(len(set(model.labels_))))
    print("Clustering doc ok !")
    
    return label_doc

def do_geo_clustering(label_tweet, geo_tweet):
    
    dataframe = pd.DataFrame(columns=['label','geo_lat','geo_long'])
    
    i = 0
    
    for (geo, label) in zip(geo_tweet, label_tweet):
#        print(geo['coordinates'])
        dataframe.loc[i] = [label, geo['coordinates'][0], geo['coordinates'][1]]
        i = i + 1

    data = dataframe.as_matrix(['geo_lat', 'geo_long'])
    
    model = DBSCAN(eps = 0.001, min_samples = 5)
    model.fit(data)
    
    label_geo = model.labels_
    print("geo : " + str(len(set(model.labels_))))
    print("Clustering geo ok !")
    
    return label_geo

def compare(label_doc, label_geo):
    
    labels = [(doc, geo) for (doc, geo) in zip(label_doc, label_geo)
              if doc != -1 and geo != -1]
        
    np.corrcoef(label_doc, label_geo)
    
    print(labels)


nb_docs = 1000
vec_dim = 2

label_tweet, text_tweet, geo_tweet, userid_tweet = get_tweet(0)

nb_docs = len(label_tweet)

label_geo = do_geo_clustering(label_tweet, geo_tweet)

#print(len(userid_tweet))
#print(userid_tweet)

label_doc = do_doc2vec(label_tweet, text_tweet)

compare(label_doc, label_geo)


#get_dendrogram(mat_docs, method = 'single')
#get_dendrogram(mat_docs, method = 'complete')
#get_dendrogram(mat_docs, method = 'ward')


