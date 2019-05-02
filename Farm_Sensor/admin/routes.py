from flask import Blueprint
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from Farm_Sensor.models import Sensor, Tank, Customer, SensorData
import random

app_module = Blueprint('admin',__name__, template_folder='templates')
class CustomerForm(FlaskForm):
    name     = StringField('name',  validators=[InputRequired(), Length(max=30)])
    address  = StringField('address',  validators=[InputRequired(), Length(max=200)])
    phone  = StringField('phone',  validators=[InputRequired(), Length(max=10)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class TankForm(FlaskForm):
    name      = StringField('name',  validators=[InputRequired(), Length(max=30)])
    latitude  = StringField('latitude',  validators=[InputRequired(), Length(max=30)])
    longitude = StringField('longitude',  validators=[InputRequired(), Length(max=30)])
    capacity  = StringField('capacity',  validators=[InputRequired(), Length(max=30)])

#admin dashboard
@app_module.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    # validte admin user
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))

    customerForm  = CustomerForm()
    tankForm = TankForm()
    msg = ''
    return render_template('admin/dashboard.html',
    name=current_user.name, 
    customers=Customer.objects().all(),
    form = customerForm ,
    message=msg,
    tankForm=tankForm,
    alltanks= getAllTanks())

# Creates new user
@app_module.route('/create/customer',methods=['GET', 'POST'])
@login_required
def createCustomer():
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    form  = CustomerForm()
    if request.method == 'POST':#check for form
        if form.validate():
            #try:
            newCustomer = Customer(password=generate_password_hash(form.password.data, method='sha256'),
                name=form.name.data, address=form.address.data,phone=form.phone.data,tanks=[]).save()
            return redirect(url_for('admin.customerDashboard', customerID=newCustomer.customerId))
            #except:
            #msg = 'User creation Failed'
        else:
            print("validation Failed")
    return redirect(url_for('admin.dashboard'))
#Creates new Tank including sensors
@app_module.route('/create/tank',methods=['GET','POST'])
@login_required
def createTank():
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    tankForm  = TankForm()
    if request.method == 'POST':#check for form
        if True:
            print("Validate")
            p = Sensor(sensorType='ph').save()
            s = Sensor(sensorType='sl').save()
            w = Sensor(sensorType='wl').save()
            tank = Tank(capacity=tankForm.capacity.data,
            latitude=tankForm.latitude.data,
            longitude=tankForm.longitude.data,
            name=tankForm.name.data,
            sensors=[p,s,w]).save()
            return redirect(url_for('admin.tankDashboard',tankID=tank.tankId))
        
    return redirect(url_for('admin.dashboard'))


# Customer detais page
@app_module.route('/customer/<customerID>')
@login_required
def customerDashboard(customerID):
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    msg= ''
    customer =  Customer.objects(customerId=customerID).first()
    return render_template('admin/customer.html',
    name=current_user.name,
    customer= customer,
    tanks=getCustomersTank(customerID),
    alltanks= getAllTanks(),
    message=msg)

#tank details page
@app_module.route('/tank/<tankID>')
@login_required
def tankDashboard(tankID):
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    msg= ''
    tank =  Tank.objects(tankId=tankID).first()
    return render_template('admin/tank.html',
    name=current_user.name,
    currentTank= tank,
    alltanks= getAllTanks(),
    message=msg)
# delete customer with id
@app_module.route('/delete/<customerID>')
@login_required
def deleteCustomer(customerID):
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    msg = ''
    try:
        customer = Customer.objects(customerId=customerID).first()
        customer.delete()
    except:
        msg = 'delete error'
    return redirect(url_for('admin.dashboard'))
    
# delete tank from customer tank list
@app_module.route('/delete/<customerID>/tank/<tankID>')
@login_required
def deleteCustomerTank(customerID,tankID):
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    msg = ''
    try:
        customer = Customer.objects(customerId=customerID).first()
        customer.tanks.remove(Tank.objects(tankId=tankID).first())
        customer.save()
        return redirect(url_for('admin.customerDashboard',customerID=customerID ))
    except:
        msg = 'delete error'
    return redirect(url_for('admin.customerDashboard',customerID=customerID ))
# add tank to customer tank list
@app_module.route('/add/<customerID>/tank/<tankID>')
@login_required
def addCustomerTank(customerID,tankID):
    if not( "admin" in current_user.role):
        return redirect(url_for('website.logout'))
    msg = ''
    try:
        customer = Customer.objects(customerId=customerID).first()
        if not Tank.objects(tankId=tankID).first() in customer.tanks:
            customer.tanks.append(Tank.objects(tankId=tankID).first())
            customer.save()
        return redirect(url_for('admin.customerDashboard',customerID=customerID ))
    except:
        msg = 'delete error'
    return redirect(url_for('admin.customerDashboard',customerID=customerID ))

def getCustomersTank(customerId):
    tanks = (Customer.objects(customerId = customerId).first()).tanks
    tanksList = []
    for tank in tanks:
        newTank = {}
        newTank["name"] = tank.name
        newTank["id"]=tank.tankId
        newTank["location"] = [tank.latitude , tank.longitude]
        for sensor in tank.sensors:
            #print("Type {}".format(sensor.sensorType))
            print(sensor.sensorId)
            if sensor.sensorType == 'ph':
                newTank["phId"] =  sensor.sensorId
            if sensor.sensorType == 'sl':
                newTank["slId"]= sensor.sensorId
            if sensor.sensorType == 'wl':
                newTank["wlId"] = sensor.sensorId
        tanksList.append(newTank)
    return  tanksList
def getAllTanks():
    tanks = Tank.objects().all()
    tanksList = []
    for tank in tanks:
        newTank = {}
        newTank["name"] = tank.name
        newTank["id"]=tank.tankId
        newTank["location"] = [tank.latitude , tank.longitude]
        for sensor in tank.sensors:
            #print("Type {}".format(sensor.sensorType))
            print(sensor.sensorId)
            if sensor.sensorType == 'ph':
                newTank["phId"] =  sensor.sensorId
            if sensor.sensorType == 'sl':
                newTank["slId"]= sensor.sensorId
            if sensor.sensorType == 'wl':
                newTank["wlId"] = sensor.sensorId
        tanksList.append(newTank)
    return  tanksList


    