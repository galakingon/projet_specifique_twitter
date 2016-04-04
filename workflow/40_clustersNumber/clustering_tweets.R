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

args <- commandArgs(trailingOnly =TRUE)
filename <- args[1]

tweets = read.csv(file = filename, header=TRUE, nrow=as.numeric(args[2]), row.names=1)
tweets <-tweets[complete.cases(tweets),]

result = data.frame(nb_clusters=c(), elbow=c(), AIC=c(), BIC=c())

for(i in 1:100)
{
fit = kmeans(x=tweets, centers=i)
aic = kmeansAIC(fit)
bic=  kmeansBIC(fit)
elbow = fit$betweenss
result<-rbind(result, data.frame(nb_clusters=c(i), elbow=c(elbow), AIC=c(aic), BIC=c(bic)))
}

#sortie, création des dossiers et des fichers 

if( substr(filename, nchar(filename)-3, nchar(filename))== ".csv"){
  filename <- substr(filename, 1, nchar(filename)-4)
}


foldername <- paste(filename, "_nb_clusters/kmeans", sep="")
dir.create(foldername, recursive=TRUE)
setwd(dir=foldername)

jpeg(paste(filename, "_bic.jpg", sep=""))
qplot(x=result["nb_clusters"], y=result["BIC"])
dev.off()

jpeg(paste(filename, "_aic.jpg", sep=""))
qplot(x=result["nb_clusters"], y=result["AIC"])
dev.off()

jpeg(paste(filename, "_elbow.jpg", sep=""))
qplot(x=result["nb_clusters"], y=result["elbow"])
dev.off()



