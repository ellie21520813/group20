import os
import json

from paho.mqtt import client as mqtt_client
from datetime import datetime
import app.db.respository.discover as DiscoverRepository

from app.db.session import get_db
from app.schemas.discover import DiscoverCreate, DiscoverShow


broker    = os.getenv("MQTT_HOST")
port      = int(os.getenv("MQTT_PORT"))
username  = os.getenv("MQTT_USER")
password  = os.getenv("MQTT_PASS")
client_id = f'device-service'

mqtt_topic_node      = f"edge/device/{id}"
mqtt_topic_node_info = f"edge/device/{id}/info"
mqtt_topic_status    = f"edge/device/{id}/status"
subscribed_topic = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("INFO:\tConnected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    def on_subscribe(client, userdata, mid, granted_qos):
        pass
    
    client = mqtt_client.Client(client_id, clean_session=True)
    client.tls_set(ca_certs="app/service/cafile.pem")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.on_subscribe = on_subscribe
    return client


def publish(client, topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def subscribe(client):
    def on_message(client, userdata, msg):
        if "edge/device/" in msg.topic:
            device = json.loads(msg.payload.decode())
            client.subscribe(f"edge/device/{device['id']}/info")
            publish(client, "server/scan", f'{device["name"]} - {datetime.now()}')
            try:
                db = next(get_db())
                device_add = DiscoverCreate(
                    device_id=device['id'],
                    name=device['name'],
                    ip=device['ip'],
                    hostname=device['hostname']
                )
                DiscoverRepository.add_new_device(discover_device=device_add, db=db)
            except Exception as e:
                print(e)
        if "edge/device/" in msg.topic and "info" in msg.topic:
            print(msg.payload.decode())

    client.subscribe("edge/device/+")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    # client.loop_start()
    subscribe(client=client)
    client.loop_forever()
