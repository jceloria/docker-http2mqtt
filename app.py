#!/usr/bin/env python3

from flask import Flask
from flask import request
import paho.mqtt.publish as publish
import os

app = Flask(__name__)


@app.route('/')
def http2mqtt():
    mqtt_host = os.environ.get('MQTT_HOST', '127.0.0.1')
    mqtt_port = os.environ.get('MQTT_PORT', 1883)

    try:
        base_topic = os.environ.get('BASE_TOPIC').strip('/')
        topic = '{}/{}/state'.format(base_topic, request.args.get('device'))
        message = request.args.get('message')
        publish.single(topic, message, hostname=mqtt_host, port=int(mqtt_port))
    except Exception:
        print("Unable to publish message, ensure `BASE_TOPIC` environment variable is set")
        pass

    return dict(topic=topic, message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
