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


def str2float(v):
    try:
        float(v)
        return float(v)
    except ValueError:
        return v


@app.route('/')
def http2mqtt():
    mqtt_host = os.environ.get('MQTT_HOST', '127.0.0.1')
    mqtt_port = os.environ.get('MQTT_PORT', 1883)
    base_topic = os.environ.get('BASE_TOPIC').strip('/')
    retain = str2bool(os.environ.get('RETAIN', '1'))

    payload = ''

    try:
        data = dict(request.args)

        device = data.pop('device')
        payload = json.dumps({k: str2float(v) for k, v in data.items()})

        topic = '{}/{}/state'.format(base_topic, device)

        app.logger.info('Publishing {} to topic {}.'.format(payload, topic))
        publish.single(topic, payload, hostname=mqtt_host, port=int(mqtt_port), retain=retain)

    except Exception as e:
        print('Unable to publish message: {}'.format(e))
        pass

    return payload


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
