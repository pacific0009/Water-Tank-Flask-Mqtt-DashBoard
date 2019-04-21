from flask import Flask
from Farm_Sensor.web_site.routes import app_module as web_site
from Farm_Sensor.web_site.routes import login_manager
from Farm_Sensor.models import db
from flask_bootstrap import Bootstrap
#from flask_mongoengine import MongoEngineSessionInterface

app = Flask(__name__)
#
# Add/register blueprint components
#
app.register_blueprint(web_site)
#
# add here all your app configuration key value
#
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '<your db url>'
}
app.config['SECRET_KEY'] = 'thisismysecrattekey' 
#app.session_interface = MongoEngineSessionInterface(db)
db.init_app(app) # initalizing DB
login_manager.init_app(app)
login_manager.login_view = 'website.login' #redirects to login view on logout
Bootstrap(app)

