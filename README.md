# Flask-Mqtt-DashBoard
Flask App, Blueprint , mongodb, Dashboard for displaying Ph data of a Customer  

Inslallation
--------------
1. Install all the dependencies from requirements.txt using $ pip instlall <dependency name>
2. Update your db host url and port in Farm_sensor/__init__.py 
3. Update your db collection in Farm_sensor/models.py 

Run
--------------
1. To run the project use command $ python run.py
2. Open browser and localhost:5000/login
3. To populate sample data modify collection as test1,test2.. in Farm_sensor/models.py and re-run the app 
and in browser type localhost:5000/populatedata


