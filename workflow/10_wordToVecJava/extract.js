db = db.getSiblingDB('projet_specifique')
cursor = db.getCollection('tweets').find({},{'text':1})
while(cursor.hasNext()){
    print(cursor.next());
}
