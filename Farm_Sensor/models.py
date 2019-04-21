from flask_mongoengine import  Document
from flask_mongoengine import MongoEngine
from flask_login import UserMixin
import datetime
db = MongoEngine()
#
# Add here your database models same as your tables in database
#
#
#
class Sensor(db.Document):
    # Sensors info table
    meta = {'collection': 'test3'}
    sensorId = db.IntField(unique = True)
    sensorType = db.StringField()
    purchaseDate = db.DateTimeField(default=datetime.datetime.utcnow)

class SensorData(db.Document):
    # Sensors data table
    meta = {'collection': 'test2'}
    sensorId = db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE)
    sensorValue = db.StringField()
    
class Tank(db.Document):
    # Tank info table
    meta = {'collection': 'test1'}
    tankId = db.IntField(unique = True)
    capacity = db.IntField()
    latitude = db.StringField()
    longitude = db.StringField()
    name = db.StringField()
    sensors = db.ListField(db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE)) #A list of reference to sensors belongs to this tank

class Customer(UserMixin, db.Document):
    #customer details table 
    meta = {'collection': 'test'}
    customerId = db.SequenceField(required=True, unique=True)
    password = db.StringField()
    name = db.StringField()
    address = db.StringField()
    phone = db.StringField()
    tanks = db.ListField(db.ReferenceField(Tank,reverse_delete_rule=db.CASCADE))



