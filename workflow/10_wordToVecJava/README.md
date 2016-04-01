# wordToVec mit Java

args[0] word vectors (csv expected, first column : words, rest : coordonates) 
args[1] tweets (1 line, 1 tweet)
args[2] out file name 
args[3] [tfidf/hashtags] ponderation
args[4] hashtags file (not available yet)

java -jar DocumentVectorGenerator.jar ../../data/vec.csv ../../data/tweets_processed.csv ../../out/vecteurs_java_tfidf.csv tfidf

