library(wordcloud)
library(tm)
library(cluster)

setwd("../../out")

args <- commandArgs(trailingOnly =TRUE)
filename = args[1]
nb_clusters = args[2]
nb_tweets = args[3]

tweets <- read.csv(filename, header = TRUE, sep = ",", nrows = nb_tweets, row.names =1)
tweets <- tweets[, -102]
tweets <- tweets[complete.cases(tweets),]
tweets <- tweets[!duplicated(tweets$text),]

drops<- c("id", "texte")
vectors <- tweets[,!names(tweets) %in% drops]
exp = 2
step = 0.1
print("pret pour clustering")
fuzzy <- NULL
repeat
{
  mess = paste("clustering avec pour valeur de exp ", as.character(exp), sep = "")
  print(mess)
  fuzzy = fanny(vectors, nb_clusters, memb.exp = exp)
  exp <- exp -step
  if(fuzzy$k.crisp == nb_clusters)
    break
}

tweets <- cbind(tweets, "clusters" = c(fuzzy$clustering))

if( substr(filename, nchar(filename)-3, nchar(filename))== ".csv")
{
  filename <- substr(filename, 1, nchar(filename)-4)
}

foldername <- paste(filename, "_wordclouds", sep="")
dir.create(foldername, recursive=TRUE)
setwd(dir=foldername)

i = 1
for(i in 1:nb_clusters)
{
  extract <- tweets[tweets$clusters==i,]
  words <- Corpus(VectorSource(extract["texte"]))
  
  current_filename <- paste(filename, "_cluster_", sep = "")
  current_filename <- paste(current_filename, as.character(i), sep = "")
  
  pdf(paste(current_filename, ".pdf", sep=""))
  wordcloud(words, scale=c(5,0.5), max.words=100, random.order=FALSE, rot.per=0.35, use.r.layout=FALSE, colors=brewer.pal(8, "Dark2"))
  dev.off()
}


