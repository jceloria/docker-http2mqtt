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


def str2bool(v):
    return str(v).lower() in ('yes', 'true', 'y', 't', '1')


@app.route('/')
def http2mqtt():
    mqtt_host = os.environ.get('MQTT_HOST', '127.0.0.1')
    mqtt_port = os.environ.get('MQTT_PORT', 1883)

    try:
        base_topic = os.environ.get('BASE_TOPIC').strip('/')
        retain = str2bool(os.environ.get('RETAIN', '1'))
        dev = request.args.get('dev')
        batt = float(request.args.get('batt'))
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        acc = float(request.args.get('acc'))
        topic = '{}/{}/state'.format(base_topic, dev)
        app.logger.info('{}, {}, {}, {}, {}'.format(dev, batt, lat, lon, acc))
        payload = json.dumps(dict(battery_level=batt, latitude=lat, longitude=lon, gps_accuracy=acc))
        publish.single(topic, payload, hostname=mqtt_host, port=int(mqtt_port), retain=retain)
    except Exception as e:
        print('Unable to publish message: {}'.format(e))
        pass

    return payload


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
