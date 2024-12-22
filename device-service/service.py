from app.service.mqtt_v2 import MQTTService
import time

mqtt_service = MQTTService()
mqtt_service.connect()
mqtt_service.start()

while True:
    time.sleep(1)