#!/usr/bin/env python3

from flask import Flask
from flask import request
import json
import logging
import os
import paho.mqtt.publish as publish

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/')
def http2mqtt():
    mqtt_host = os.environ.get('MQTT_HOST', '127.0.0.1')
    mqtt_port = os.environ.get('MQTT_PORT', 1883)

    try:
        base_topic = os.environ.get('BASE_TOPIC').strip('/')
        topic = '{}/{}/state'.format(base_topic, request.args.get('device'))
        batt = request.args.get('battery')
        lat = request.args.get('latitude')
        lon = request.args.get('longitude')
        acc = request.args.get('accuracy')
        payload = json.dumps(dict(battery=batt, latitude=lat, longitude=lon, gps_accuracy=acc))
        app.logger.info(payload)
        publish.single(topic, payload, hostname=mqtt_host, port=int(mqtt_port))
    except Exception as e:
        print("Unable to publish message: {}".format(e))
        pass

    return payload


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
