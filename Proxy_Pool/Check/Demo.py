from DB import MongodbClient

db = MongodbClient('useful_proxy', 'localhost', 27017)
db.pop(10)
