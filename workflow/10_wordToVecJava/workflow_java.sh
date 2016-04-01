#README !!!

#script d'exécution du workflow 
# 1 - extraction depuis mongodb
# 2 - word vector avec word2vec
# 3 - document vector avec un programme java 
#  sortie : csv avec 1 : id, 2 : texte du tweet, 3...dim+3 : vecteur
# arg1 : [skip|clean|extract]
# arg2 : [tfidf|hashtags]
# arg3 : output file name
# arg4 : dimension


DATA=../../data
OUT=../../out
WORD2VEC=word2vec/word2vec
TWEETS=tweets.txt
WVEC=word_vectors.csv
HASHTAGS=hashtags.txt
EXTRACT_MAIN=extract.js
EXTRACT_HASHTAGS=extract_hashtags.js
jAVA="java - jar DocumentVectorGenerator.jar"
MODE=$1
PONDER=$2
OUTPUT=$3
DIM=${4-100}


if [$(MODE)=clean]
then
	rm $(DATA)/$(TWEETS)
	rm $(DATA)/$(WVEC)
	rm $(DATA)/$(HASHTAGS)
	mongo --quiet $(EXTRACT_MAIN) > $(DATA)/$(TWEETS)

WORD2VEC -train $(DATA)/$(TWEETS) -output $(DATA)/$(WVEC) -size $(DIM)

if [$(PONDER)=hashtags]
then 
	mongo --quiet $(EXTRACT_HASHTAGS) > $(DATA)/$(HASHTAGS)
	$(JAVA) $(DATA)/$(WVEC) $(DATA)/$(TWEETS) $(OUT)/vecteurs_java_$(PONDER).csv -$(PONDER) $(DATA)/$(HASHTAGS)
elif [$(PONDER)=tfidf]
then	
	$(JAVA) $(DATA)/$(WVEC) $(DATA)/$(TWEETS) $(OUT)/vecteurs_java_$(PONDER).csv -$(PONDER)


