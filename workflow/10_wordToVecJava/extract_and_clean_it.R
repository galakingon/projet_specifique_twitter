library(rmongodb)
library(tm)
library(SnowballC)

frenchStemming = function(x)
{
  vec <- strsplit(x, " ")
  stemmed <- wordStem(unlist(vec), "french")
  while(!isTRUE(all.equal(unlist(vec), unlist(stemmed))))
  {
    vec <- stemmed
    stemmed <- wordStem(unlist(vec), "french")
  }
  vec <- paste(unlist(vec), collapse = " ")
  return(paste(vec, "\n\r", sep = " "))
}


args <- commandArgs(trailingOnly =TRUE)
cleaning_options = args[1]

mongo <- mongo.create()
tweets <- data.frame()
if(mongo.is.connected(mongo) == TRUE)
{
  tweets<- mongo.find.all(mongo, "projet_specifique.tweets", fields='{"_id":1, "text":1}', data.frame = TRUE)
}

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

