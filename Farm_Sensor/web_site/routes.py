from flask import Blueprint
from flask import jsonify
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

# root page set as dashbord
@app_module.route('/')
@login_required
def ind():
    #return redirect( url_for('static', filename='index.html'))
    avgPH, avgSalinity, avgWater = getAvgOfTanksForCurrent_User()
    return render_template('index.html',
    name=current_user.name, 
    tanksTable= prepareTableDataForCurrent_user(),
    avgPH= avgPH,
    avgSalinity= avgSalinity,
    avgWater=avgWater)

#login page 
@app_module.route('/login', methods=['GET', 'POST'])
def login():
    # Login page Handler
    msg = '' #message to user on incorrect login credentials
    if current_user.is_authenticated == True:
        # if authorised redirect to dashboard 
        return redirect(url_for('website.dashboard'))
    form = RegForm()
    if request.method == 'POST':#check for form
        if form.validate():
            print("getting user")
            # validate user
            check_user = Customer.objects(customerId=form.username.data).first()
            msg = "Customer not exist!"
            if check_user:
                print("Found")
                #verify password
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    # Open Dashboard page
                    try:
                        if "admin" in current_user.role:
                            return redirect('admin/dashboard')
                    except:
                        print("Exception in role")
                    return redirect(url_for('website.dashboard'))
                msg = "Incorrect Customer Id or  password!"
    return render_template('login.html', form=form , message = msg)

@app_module.route('/dashboard')
@login_required
def dashboard():
    avgPH, avgSalinity, avgWater = getAvgOfTanksForCurrent_User() #calculate average % of data
    return render_template('index.html',
    name=current_user.name, 
    tanksTable= prepareTableDataForCurrent_user(),
    avgPH= avgPH,
    avgSalinity= avgSalinity,
    avgWater=avgWater)

@app_module.route('/tank/<ID>')
@login_required
def tankView(ID):
    tankData = getTankdata(ID)
    return render_template('tankview.html',
    customerName=current_user.name,
    tankData=tankData)
#
# return tank data in json form 
# used in tankview jqury to get latest data
#
@app_module.route('/tankdata/<ID>')
@login_required
def tankDataInfoAsHTML(ID):
    return jsonify( getTankdata(ID))
#
# Logout Handler
#
@app_module.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('website.login'))

def getAvgOfTanksForCurrent_User(): 
    #
    # Modify this function for avg sensor value (of dashboard) 
    #
    totalPH = 0
    totalSalinity = 0
    totalWater = 0
    totalTanks = len(current_user.tanks)

    for tank in current_user.tanks:
        # loop through all takns belongs to curent user
        for sensor in tank.sensors:
            # loop through all sensor in Tank 
            print(sensor.id)
            # get sensor value
            sensorValue = (SensorData.objects(sensorId=sensor).first()).sensorValue
            # suming sensor values
            # Replce with your logic for average calculation 
            #
            if sensor.sensorType == 'ph':
                totalPH = totalPH + float(sensorValue)
            if sensor.sensorType == 'sl':
                totalSalinity = totalSalinity + float(sensorValue)
            if sensor.sensorType == 'wl':
                totalWater = totalWater + float(sensorValue)
    return round(totalPH/totalTanks,2), round(totalSalinity/totalTanks,2) ,round(totalWater/totalTanks, 2)  


def prepareTableDataForCurrent_user(startIndex=0, nuberOfItem=1000):
    #
    # Prepare dashboard table data here
    # Returns list of tanks dict with tank propertis 
    # Limit the output list by giving the start index and maximum requied numberOfItem fom Tanks of current user
    #
    tankTable = []
    count = 0
    for tank in current_user.tanks[startIndex:startIndex+nuberOfItem]:
        count = count +1
        newTank = {}
        newTank["tankNumber"] = startIndex+count
        newTank["id"]=tank.tankId
        newTank["name"] = tank.name
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
    
def getTankdata(id):
    #
    # prepare data for rendering html template for tankboard
    #
    tank = Tank.objects(tankId=id).first()
    print(id)
    print(tank)
    newTank = {}
    newTank["name"] = tank.name
    newTank["id"]=tank.tankId
    newTank["location"] = [tank.latitude , tank.longitude]
    for sensor in tank.sensors:
        sensorValue = (SensorData.objects(sensorId=sensor).order_by('-id').first()).sensorValue
        #print("Type {}".format(sensor.sensorType))
        print(sensor.sensorId)
        if sensor.sensorType == 'ph':
            newTank["ph"] =  sensorValue
        if sensor.sensorType == 'sl':
            newTank["salinity"]= sensorValue
        if sensor.sensorType == 'wl':
            newTank["water"] = sensorValue
    return  newTank