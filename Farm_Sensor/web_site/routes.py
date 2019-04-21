from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from Farm_Sensor.models import Sensor, Tank, Customer, SensorData
import random
login_manager = LoginManager()

app_module = Blueprint('website',__name__, template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return Customer.objects(pk=user_id).first()

class RegForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

@app_module.route('/login', methods=['GET', 'POST'])
def login():
    # Login page Handler
    if current_user.is_authenticated == True:
        # if authorised redirect to dashboard 
        return redirect(url_for('website.dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            print("getting user")
            # validate user
            check_user = Customer.objects(customerId=form.username.data).first()
            if check_user:
                print("Found")
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('website.dashboard'))
    return render_template('login.html', form=form)

@app_module.route('/dashboard')
@login_required
def dashboard():
    avgPH, avgSalinity, avgWater = getAvgOfTanksForCurrent_User()
    return render_template('dashboard.html',
    name=current_user.name, 
    tanksTable= prepareTableDataForCurrent_user(),
    avgPH= avgPH,
    avgSalinity= avgSalinity,
    avgWater=avgWater)

@app_module.route('/tank/<ID>')
@login_required
def tankboard(ID):
    ph, salinity, water = prepareTankdata(ID)
    return render_template('tankboard.html',
    name=current_user.name, 
    avgPH= ph,
    avgSalinity= salinity,
    avgWater=water)

@app_module.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('website.login'))

def getAvgOfTanksForCurrent_User(): 
    #
    # Modify this function for avg sensor value for dashboard 
    #
    totalPH = 0
    totalSalinity = 0
    totalWater = 0
    totalTanks = len(current_user.tanks)

    for tank in current_user.tanks:
        # loop through all takns belongs to curent user
        for sensor in tank.sensors:
            print(sensor.id)
            sensorValue = (SensorData.objects(sensorId=sensor).first()).sensorValue
            if sensor.sensorType == 'ph':
                totalPH = totalPH + float(sensorValue)
            if sensor.sensorType == 'sl':
                totalSalinity = totalSalinity + float(sensorValue)
            if sensor.sensorType == 'wl':
                totalWater = totalWater + float(sensorValue)
    return totalPH/totalTanks, totalSalinity/totalTanks , totalWater/totalTanks  

def prepareTableDataForCurrent_user(startIndex=0, nuberOfItem=10):
    #
    # Prepare dashboard table data here
    # 
    tankTable = []
    count = 0
    for tank in current_user.tanks[startIndex:startIndex+nuberOfItem]:
        count = count +1
        newTank = {}
        newTank["tankNumber"] = startIndex+count
        newTank["id"]=tank.tankId
        newTank["location"] = tank.latitude + ", "+tank.longitude
        for sensor in tank.sensors:
            sensorValue = (SensorData.objects(sensorId=sensor).first()).sensorValue
            #print("Type {}".format(sensor.sensorType))
            if sensor.sensorType == 'ph':
                newTank["ph"] =  sensorValue
            if sensor.sensorType == 'sl':
                newTank["salinity"]= sensorValue
            if sensor.sensorType == 'wl':
                newTank["water"] = sensorValue
        tankTable.append(newTank)
    print(tankTable)
    return tankTable
    
def prepareTankdata(id):
    #
    # prepare data for rendering html template for tankboard
    #
    tank = Tank.objects(tankId=id).first()
    print(id)
    print(tank)
    newTank = {}
    newTank["tankNumber"] = tank.tankId
    newTank["id"]=tank.tankId
    newTank["location"] = tank.latitude + ", "+tank.longitude
    for sensor in tank.sensors:
        sensorValue = (SensorData.objects(sensorId=sensor).first()).sensorValue
        #print("Type {}".format(sensor.sensorType))
        if sensor.sensorType == 'ph':
            newTank["ph"] =  sensorValue
        if sensor.sensorType == 'sl':
            newTank["salinity"]= sensorValue
        if sensor.sensorType == 'wl':
            newTank["water"] = sensorValue
    return  newTank["ph"],newTank["salinity"],newTank["water"]


@app_module.route('/populatedata')
def populatedata():
    # populate data in database 
    # don't run call more than one it will give you error for duplicate entry
    # or modify to add your data 
    # Type   - Sensor 
    #   ph   - pH
    #   sl   - salinity
    #   wl   - water level

    s1=Sensor(10001,'ph').save()# first argument is sensor Id and second is sensor type 
    s2=Sensor(10002,'sl').save()
    s3=Sensor(10003,'wl').save()
    s4=Sensor(10004,'ph').save()
    s5=Sensor(10005,'sl').save()
    s6=Sensor(10006,'wl').save()
    s7=Sensor(10007,'ph').save()
    s8=Sensor(10008,'sl').save()
    s9=Sensor(10009,'wl').save()
    s10=Sensor(10010,'ph').save()
    s11=Sensor(10011,'sl').save()
    s12=Sensor(10012,'wl').save()
    s13=Sensor(10013,'ph').save()
    s14=Sensor(10014,'sl').save()
    s15=Sensor(10015,'wl').save()

    for sensor in Sensor.objects:
        print("woring")
        #populating sensorData table
        SensorData(sensor, str(random.randint(1,100))).save()# first arg is refrence to sensor and second is sensor value

    t1=Tank(1001,500,'-17.0299302','23.2343432','name1',[s1,s2,s3]).save()
    t2=Tank(1002,500,'-17.0299302','23.2343432','xcc2',[s4,s5,s6]).save()
    t3=Tank(1003,500,'-17.0299302','23.2343432','name3',[s7,s8,s9]).save()
    t4=Tank(1004,500,'-17.0299302','23.2343432','xcc4',[s10,s11,s12]).save()
    t5=Tank(1005,500,'-17.0299302','23.2343432','name5',[s13,s14,s15]).save()
    #t6=Tank(1006,500,'-17.0299302','23.2343432','xcc6',[s1,s2]).save()

    #Customer(1000000001,generate_password_hash('12341234', method='sha256'),'Anand', 'address','78473574357',[t1]).save()
    Customer(password=generate_password_hash('12341234', method='sha256'),
    name='abhilash', address='cbgfd',phone='67576567',tanks=[t2 for t2 in Tank.objects]).save()
    Customer(password=generate_password_hash('12341234', method='sha256'),
    name='ramprakas', address='cbgfd',phone='67576567',tanks=[t2 for t2 in Tank.objects]).save()
    Customer(password=generate_password_hash('12341234', method='sha256'),
    name='abhilash1', address='cbgfd',phone='67576567',tanks=[t2 for t2 in Tank.objects]).save()
    Customer(password=generate_password_hash('12341234', method='sha256'),
    name='abhilash2', address='cbgfd',phone='67576567',tanks=[t2 for t2 in Tank.objects]).save()
    Customer(password=generate_password_hash('12341234', method='sha256'),
    name='abhilash3', address='cbgfd',phone='67576567',tanks=[t2 for t2 in Tank.objects]).save()
 
    for user in Customer.objects:
        print(user.customerId)
        print(user.name)
        for tank in user.tanks:
            print(tank.name)
    return "Sucess"