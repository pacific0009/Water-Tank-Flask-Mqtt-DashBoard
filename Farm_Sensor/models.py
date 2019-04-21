from flask_mongoengine import  Document
from flask_mongoengine import MongoEngine
from flask_login import UserMixin
import datetime
db = MongoEngine()

class Sensor(db.Document):
    meta = {'collection': 'Sensor3'}
    sensorId = db.IntField(unique = True)
    sensorType = db.StringField()
    purchaseDate = db.DateTimeField(default=datetime.datetime.utcnow)

class SensorData(db.Document):
    meta = {'collection': 'SensorData3'}
    sensorId = db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE)
    sensorValue = db.StringField()
    
class Tank(db.Document):
    meta = {'collection': 'Tank3'}
    tankId = db.IntField(unique = True)
    capacity = db.IntField()
    latitude = db.StringField()
    longitude = db.StringField()
    name = db.StringField()
    sensors = db.ListField(db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE))

class Customer(UserMixin, db.Document):
    meta = {'collection': 'Customer3'}
    customerId = db.SequenceField(required=True, unique=True)
    password = db.StringField()
    name = db.StringField()
    address = db.StringField()
    phone = db.StringField()
    tanks = db.ListField(db.ReferenceField(Tank,reverse_delete_rule=db.CASCADE))



