library(rmongodb)

setwd("/media/paul/Seagate Backup Plus Drive/projet_specifique_twitter/data")

mongo <- mongo.create()
hashtags <- data.frame()
if(mongo.is.connected(mongo) == TRUE)
{
  hashtags<- mongo.find.all(mongo, "projet_specifique.tweets", fields='{"_id":1, entities.hashtags":1}', data.frame = TRUE)
}
