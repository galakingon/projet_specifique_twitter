kmeansAIC = function(fit){
  
  m = ncol(fit$centers)
  n = length(fit$cluster)
  k = nrow(fit$centers)
  D = fit$tot.withinss
  return(D + 2*m*k)
}

kmeansBIC = function(fit){
  
  m = ncol(fit$centers)
  n = length(fit$cluster)
  k = nrow(fit$centers)
  D = fit$tot.withinss
  return(D + log(n)*m*k)
}

setwd(dir = "../../out")

library(stats)
library(ggplot2)
library(dbscan)

args <- commandArgs(trailingOnly =TRUE)
filename <- args[1]
nb_tweets<- as.numeric(args[2])

tweets = read.csv(file = filename, header=TRUE, nrow=nb_tweets, row.names=1)
tweets <- tweets[,-102]
tweets <-tweets[complete.cases(tweets),]
drops <- c("texte")
vectors <- tweets[ , !(names(tweets) %in% drops)]

result_kmeans = data.frame(nb_clusters=c(), elbow=c(), AIC=c(), BIC=c())
#result_dbscan = data.frame(eps=c(), nb_clusters=c(), minpts=c())

for(i in 2:100)
{
  fit = kmeans(x=vectors, centers=i)
  aic = kmeansAIC(fit)
  bic=  kmeansBIC(fit)
  elbow = fit$tot.withinss
  result_kmeans<-rbind(result_kmeans, data.frame(nb_clusters=c(i), elbow=c(elbow), AIC=c(aic), BIC=c(bic)))
}

# for(y in seq(0 , 1 , by=0.01))
# {
#   for(minp in seq(0.2, 2, by=0.1))
#   {
#     fit = dbscan(x = tweets, eps = y, minPts = minp*nb_tweets)
#     result_dbscan<-rbind(result_dbscan, data.frame(eps=c(y), nb_clusters=c(length(unique(fit$cluster))), minpts=c(minp)))
#   }
# }
#sortie, création des dossiers et des fichers 

if( substr(filename, nchar(filename)-3, nchar(filename))== ".csv")
{
  filename <- substr(filename, 1, nchar(filename)-4)
}


#k means
foldername <- paste(filename, "_nb_clusters/kmeans", sep="")
dir.create(foldername, recursive=TRUE)
setwd(dir=foldername)

jpeg(paste(filename, "_bic.jpg", sep=""))
qplot(x=result_kmeans["nb_clusters"], y=result_kmeans["BIC"])
dev.off()

jpeg(paste(filename, "_aic.jpg", sep=""))
qplot(x=result_kmeans["nb_clusters"], y=result_kmeans["AIC"])
dev.off()

jpeg(paste(filename, "_elbow.jpg", sep=""))
qplot(x=result_kmeans["nb_clusters"], y=result_kmeans["elbow"])
dev.off()

# setwd(dir="../..")
# foldername <- paste(filename, "_nb_clusters/dbscan", sep="")
# dir.create(foldername, recursive=TRUE)
# setwd(dir=foldername)

# 
# #dbscan
# jpeg(paste(filename, "_eps.jpg", sep=""))
# qplot(x=result_dbscan["eps"], y=result_dbscan["nb_clusters"], data=result_dbscan, colour=result_dbscan["minpts"])
# dev.off()


