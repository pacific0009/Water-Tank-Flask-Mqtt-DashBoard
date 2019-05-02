import dash
from flask import Flask
from Farm_Sensor.web_site.routes import app_module as web_site
from Farm_Sensor.web_site.routes import login_manager, login_required
from Farm_Sensor.admin.routes import app_module as web_admin
from Farm_Sensor.models import db, clearAndPopulateDb, createAdminUser
from flask_bootstrap import Bootstrap
from Farm_Sensor.MqttHandler import mqtt
from flask.helpers import get_root_path

#from flask_mongoengine import MongoEngineSessionInterface

app = Flask(__name__)
#
# Add/register blueprint components
#

def appConfigurations():
    #
    # add here all your app configuration key value
    #
    app.config['MONGODB_SETTINGS'] = {
        'db': 'test',
        'host': 'mongodb://admin:root@localhost:27017/admin'
    }
    app.config['SECRET_KEY'] = '<thisismysecrattekey>' # use your secrate key 
    app.config['MQTT_BROKER_URL'] = '< Your Broker url>'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = '<mqtt userid>'  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = '<mqtt password>'  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False 

def initalizingExtentions():
    #
    # Add all extension initializations here 
    #
    app.register_blueprint(web_site) # registering blue_print module named website
    app.register_blueprint(web_admin, url_prefix="/admin") # registering blue_print module named website

    db.init_app(app) # initalizing DB
    #populteDatabase() #Uncomment this to populate sample data in database.
    login_manager.init_app(app) 
    login_manager.login_view = 'website.login' #redirects to login view on logout
    Bootstrap(app) # Bootstrap for Jinja template rendering with boot strap

    registerDashApp(app) # python dash app 
    mqtt.init_app(app)   # Mqtt client  

def populteDatabase():
    #try:
    clearAndPopulateDb()
    createAdminUser() #Uncomment this to create admin user
    #except:
    print("DB entry error")
def registerDashApp(dashapp):
    from Farm_Sensor.dashapp1.layout import layout
    from Farm_Sensor.dashapp1.callbacks import register_callbacks
    
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    
    dashapp1 = dash.Dash(__name__,
                         server=dashapp,
                         url_base_pathname='/dash/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])
        
    dashapp1.title = 'Dashapp 1'
    dashapp1.layout = layout
    register_callbacks(dashapp1)
    _protect_dashviews(dashapp1)

def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])



