library(wordcloud)
library(tm)
library(cluster)

args <- commandArgs(trailingOnly =TRUE)
filename = args[1]
nb_clusters = args[2]
nb_tweets = args[3]

tweets <- read.csv(filename, header = TRUE, sep = ",", )

tweets <- tweets[complete.cases(tweets),]
tweets <- tweets[!duplicated(tweets$text),]


if(args[1] == "dirty")
{
  words <- Corpus(VectorSource(tweets["text"]))
  writeCorpus(words, ".", c("tweets.txt"))
}

if(args[1]== "clean") 
{
  words <- Corpus(VectorSource(tweets["text"]))
  words <- tm_map(words, stripWhitespace, lazy=TRUE)
  words <- tm_map(words, removePunctuation, lazy=TRUE)
  words <- tm_map(words, tolower, lazy=TRUE)
  words <- tm_map(words, PlainTextDocument, lazy=TRUE)
  words <- tm_map(words, removeWords, stopwords("french"), lazy=TRUE)
  remove_url <- function(x) gsub("http\\w+ *", "", x) 
  words <- tm_map(words, remove_url)
  words <- tm_map(words, stemDocument)
  words <- tm_map(words, PlainTextDocument, lazy=TRUE)
  writeCorpus(words, ".", c("tweets.txt"))
}

  
if(args[1]== "lyon")
{
  words <- Corpus(VectorSource(tweets["text"]))
  words <- tm_map(words, stripWhitespace, lazy=TRUE)
  words <- tm_map(words, removePunctuation, lazy=TRUE)
  words <- tm_map(words, tolower, lazy=TRUE)
  words <- tm_map(words, PlainTextDocument, lazy=TRUE)
  words <- tm_map(words, removeWords, stopwords("french"), lazy=TRUE)
  remove_url <- function(x) gsub("http\\w+ *", "", x)
  words <- tm_map(words, remove_url)
  words <- tm_map(words, frenchStemming)
  words <- tm_map(words, removeWords, c("lyon"))
  words <- tm_map(words, PlainTextDocument, lazy=TRUE)
  writeCorpus(words, ".", c("tweets_full_cleaning.txt"))
}

