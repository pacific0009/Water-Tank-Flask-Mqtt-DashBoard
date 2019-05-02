from flask_mongoengine import  Document
from flask_mongoengine import MongoEngine
from flask_login import UserMixin
import datetime
import random
from werkzeug.security import generate_password_hash
db = MongoEngine()
#
# Add here your database models same as your tables in database
#
#
#
class Sensor(db.Document):
    # Sensors info table
    meta = {'collection': 'sensor'}
    sensorId =  db.SequenceField(required=True, unique=True)
    sensorType = db.StringField()
    purchaseDate = db.DateTimeField(default=datetime.datetime.utcnow)

class SensorData(db.Document):
    # Sensors data table
    meta = {'collection': 'sensordata'}
    sensorId = db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE)
    sensorValue = db.StringField()
    
class Tank(db.Document):
    # Tank info table
    meta = {'collection': 'tank'}
    tankId =  db.SequenceField(required=True, unique=True)
    capacity = db.IntField()
    latitude = db.StringField()
    longitude = db.StringField()
    name = db.StringField()
    sensors = db.ListField(db.ReferenceField(Sensor,reverse_delete_rule=db.CASCADE)) #A list of reference to sensors belongs to this tank

class Customer(UserMixin, db.Document):
    #customer details table 
    meta = {'collection': 'customer'}
    customerId = db.SequenceField(required=True, unique=True)
    password = db.StringField()
    name = db.StringField()
    address = db.StringField()
    phone = db.StringField()
    tanks = db.ListField(db.ReferenceField(Tank,reverse_delete_rule=db.CASCADE))
    role  = db.ListField(db.StringField())


def saveSensorDataReceivedFromMqtt(data):
    #
    # data is dict contains topic and payload
    # payload is sensor value
    #
    item = data["topic"].split("/") # split topic to get customer id, tank id and sensor id
    print (item)

    # verify customer id in db 
    cust = Customer.objects(customerId=int(item[1])).first() 
    if(cust):
        print("Customer Found {}".format(cust.customerId))
        #Verify Sensor id in db
        sensor = Sensor.objects(sensorId = int(item[3])).first() 
        if(sensor):
            print("Sensor Found ")
            # storing data to Sensor data
            SensorData(sensor,data["payload"]).save()
    else:
        print("Customer not found")
    print("All Set")

def clearAndPopulateDb():
    # This function populate sample data in database 
    # I will be affective only if you drop all your collections manually
    # don't run call more than one it will give you error for duplicate entry
    # or modify to add your data 
    # Type   - Sensor 
    #   ph   - pH
    #   sl   - salinity
    #   wl   - water level
    print("Populating "+"."*40)
    for x in range(99):
        p = Sensor(sensorType='ph').save()
        s = Sensor(sensorType='sl').save()
        w = Sensor(sensorType='wl').save()
        Tank(capacity=500,
        latitude=str(17.0299302 + random.randint(0,4)),
        longitude=str(23.2343432+random.randint(0,4)),
        name='name'+str(x),
        sensors=[p,s,w]).save()
    
        

    for sensor in Sensor.objects:
        #populating sensorData table
        SensorData(sensor, str(random.randint(1,100))).save()# first arg is refrence to sensor and second is sensor value

    #Customer(1000000001,generate_password_hash('12341234', method='sha256'),'Anand', 'address','78473574357',[t1]).save()
    for x in range(10):
        Customer(password=generate_password_hash('12341234', method='sha256'),
        name='abhilash', address='cbgfd',phone='67576567',tanks=[t2 for i, t2 in enumerate(Tank.objects) if i < random.randint(50,70)]).save()
        Customer(password=generate_password_hash('12341234', method='sha256'),
        name='ramprakas', address='cbgfd',phone='67576567',tanks=[t2 for i, t2 in enumerate(Tank.objects) if i > random.randint(0,60)]).save()
        Customer(password=generate_password_hash('12341234', method='sha256'),
        name='abhilash1', address='cbgfd',phone='67576567',tanks=[t2 for i, t2 in enumerate(Tank.objects) if i < random.randint(20,70)]).save()
        Customer(password=generate_password_hash('12341234', method='sha256'),
        name='abhilash2', address='cbgfd',phone='67576567',tanks=[t2 for i, t2 in enumerate(Tank.objects) if i < random.randint(60,70)]).save()
        Customer(password=generate_password_hash('12341234', method='sha256'),
        name='abhilash3', address='cbgfd',phone='67576567',tanks=[t2 for i, t2 in enumerate(Tank.objects) if i > random.randint(30,50)]).save()
 
    for user in Customer.objects:
        print("CustomerID: {} Created".format(user.customerId))
        """print(user.name)
        for tank in user.tanks:
            print(tank.name)"""
    print("End Data Population" + "."*40 )
    return "Sucess"
def createAdminUser():
    admin = Customer(password=generate_password_hash('1234abcd', method='sha256'),
        name='Admin', address='Your choice',phone='67576567',tanks=[],role=["admin"]).save()
    print ("admin ID {}   Pwd:1234abcd".format(admin.customerId))