library(rmongodb)
library(tm)

setwd("/media/paul/Seagate Backup Plus Drive/projet_specifique_twitter/data")

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

if(args[1]== "full")
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
}
  writeCorpus(words, ".", c("tweets.txt"))
  

