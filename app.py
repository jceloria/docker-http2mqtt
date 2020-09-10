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
    topic = request.args.get('topic')
    message = request.args.get('message')
    publish.single(topic, message, hostname=mqtt_host, port=int(mqtt_port))
    return request.args


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
