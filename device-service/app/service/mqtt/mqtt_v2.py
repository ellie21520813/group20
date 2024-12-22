import os
import json
import threading

from paho.mqtt import client as mqtt_client
from datetime import datetime
import app.db.respository.discover as DiscoverRepository
import app.db.respository.device as DeviceRepository

from app.db.session import get_db
from app.schemas.discover import DiscoverCreate, DiscoverShow
from app.schemas.device import DeviceCreate


broker    = os.getenv("MQTT_HOST")
port      = int(os.getenv("MQTT_PORT"))
username  = os.getenv("MQTT_USER")
password  = os.getenv("MQTT_PASS")
client_id = f'device-service'

mqtt_topic_node      = f"edge/device/{id}"
mqtt_topic_node_info = f"edge/device/{id}/info"
mqtt_topic_status    = f"edge/device/{id}/status"
subscribed_topic = []


class MQTTService:
    def __init__(self) -> None:
        self.broker    = os.getenv("MQTT_HOST")
        self.port      = int(os.getenv("MQTT_PORT"))
        self.username  = os.getenv("MQTT_USER")
        self.password  = os.getenv("MQTT_PASS")
        self.client_id = f'device-service'
        self.ca_file   = "app/service/cafile.pem"
        self.subscribed_topic = []
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("INFO:\tConnected to MQTT Broker!")
            self.client.subscribe("edge/device/#")

        else:
            print("Failed to connect, return code %d\n", rc)
    
    def _on_message(self, client, userdata, msg):
        print(f"[INFO]:\t Topic {msg.topic}")
        print(f"[INFO]:\t {msg.payload.decode()}")

        # if "edge/device/" in msg.topic:
        #     device = json.loads(msg.payload.decode())
        #     self.subscribe(f"edge/device/{device['id']}/status")
        if "edge/device/" in msg.topic and "/status" in msg.topic:
            device = json.loads(msg.payload.decode())
            self.publish("server/scan", f'{device["name"]} - {device["status"]} - {datetime.now()}')
            try:
                db = next(get_db())
                device_add = DiscoverCreate(
                    device_id=device['id'],
                    name=device['name'],
                    ip=device['ip'],
                    hostname=device['hostname'],
                    status=device['status']
                )

                device = DeviceCreate(
                    device_id=device['id'],
                    status=device['status']
                )
                DiscoverRepository.add_new_device(discover_device=device_add, db=db)
                DeviceRepository.add_new_device(device_add=device, db=db)
            except Exception as e:
                print(e)
        
        
        if "edge/device/" in msg.topic and "/info" in msg.topic:
            device = json.loads(msg.payload.decode())
            try:
                db = next(get_db())
                device_add = DeviceCreate(
                    device_id=device['id'],
                    name=device['name'],
                    hostname=device['hostname'],
                    ip=device['ip'],
                    machine=device['machine'],
                    version=device['version'],
                    platform=device['platform'],
                    system=device['system'],
                    processor=device['processor'],
                    cpu=device['cpu'],
                    memory=str(device['memory']),
                    status=device['status']
                )
                DeviceRepository.add_new_device(device_add=device_add, db=db)
            except Exception as e:
                print(e)

    def connect(self):
        self.client    = mqtt_client.Client(client_id=self.client_id, clean_session=True)
        self.client.tls_set(ca_certs=self.ca_file)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect_async(self.broker, self.port)
    
    def start(self):
        self.client.loop_start()

    def loop_forever(self):
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()

    def subscribe(self, topic):
        if topic not in self.subscribed_topic:
            self.client.subscribe(topic=topic)
            self.subscribed_topic.append(topic)
        else:
            print(f"[INFO]:\t Topic {topic} already subscribed")
    
    def publish(self, topic, msg, qos=0, retain=False):
        self.client.publish(topic, msg, qos,retain)


