# docker-http2mqtt - Insecure HTTP to MQTT bridge

You most likely don't want to use this, there is no security in place and it was whipped together haphazardly.
The main reason I wrote this is because I wanted to use Macrodroid to interact with bluetooth beacons and publish state to a local message broker for home automation stuff. I didn't want to use Tasker and the MQTT Publish plugin as they have both become extremely unreliable.

##### docker-compose:
```
version: "3.7"

volumes:
  mqttdata:

services:
  mosquitto:
    image: eclipse-mosquitto
    ports:
    - 18833:1883
    volumes:
    - /opt/data/mqtt/mosquitto/config:/mosquitto/config
    - mqttdata:/mosquitto/data

  http2mqtt:
    image: jceloria/http2mqtt
    environment:
    - MQTT_HOST=mosquitto
    - MQTT_PORT=18833
    - BASE_TOPIC=location
    ports:
    - 8000:8000
```

##### example:
```
$─► curl 'http://localhost:8000/?device=a1:b2:c3:d4:e5:f6&message=office'
{"message":"office","topic":"location/a1:b2:c3:d4:e5:f6/state"}
```

![Docker](https://github.com/jceloria/docker-alpine-ripper/workflows/Docker/badge.svg)
