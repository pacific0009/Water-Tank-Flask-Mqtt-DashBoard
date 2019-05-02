from flask_mqtt import Mqtt
from Farm_Sensor.models import saveSensorDataReceivedFromMqtt
mqtt = Mqtt()

#
# Call back functon when mqtt client connect to broker
#
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('tanksensor/#')

#
# Call back functon when any message arrive to subscrived topic Mqtt
#
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # On receving message
    # Verify and store received data
    #
    saveSensorDataReceivedFromMqtt(data)

