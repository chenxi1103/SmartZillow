import mongodb_client

db = mongodb_client.getDB()

#"test" is table name
db.test.insert({"name" : "chenxili"})

print list(db.test.find({"name": "chenxili"}))