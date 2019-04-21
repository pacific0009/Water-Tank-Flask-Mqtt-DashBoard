from flask import Flask
from Farm_Sensor.web_site.routes import app_module as web_site
from Farm_Sensor.web_site.routes import login_manager
from Farm_Sensor.models import db
from flask_bootstrap import Bootstrap
#from flask_mongoengine import MongoEngineSessionInterface

app = Flask(__name__)
Bootstrap(app)
app.register_blueprint(web_site)
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '<Provide your host address>'
}

app.config['SECRET_KEY'] = 'thisismysecrattekey'
db.init_app(app)
#app.session_interface = MongoEngineSessionInterface(db)

login_manager.init_app(app)
login_manager.login_view = 'website.login'
