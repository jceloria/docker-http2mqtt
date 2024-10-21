# docker-http2mqtt - Insecure HTTP to MQTT bridge

You most likely don't want to use this, there is no security in place and it was whipped together haphazardly.
The main reason I wrote this is because I wanted to send GPS/battery information from [GPSLogger](https://gpslogger.app) to [Eclipse Mosquitto™](https://mosquitto.org/).

I highly recommend against exposing this to the public internet unless you have some other controls in place.

##### docker-compose:
```
volumes:
  mqttdata:

services:
  mosquitto:
    image: docker.io/library/eclipse-mosquitto
    ports:
    - 1833:1883
    volumes:
    - /opt/data/mqtt/mosquitto/config:/mosquitto/config
    - mqttdata:/mosquitto/data

  http2mqtt:
    image: docker.io/jceloria/http2mqtt
    environment:
    - MQTT_HOST=mosquitto
    - MQTT_PORT=1833
    - BASE_TOPIC=location
    ports:
    - 8000:8000
```

##### example:
The `device` parameter is the only requirement.
```
$─► curl 'http://localhost:8000/?device=a1b2c3d4e5&latitude=-90.0000&longitude=-0.0000&gps_accuracy=90&battery_level=94'
{"latitude": -90.0, "longitude": -0.0, "gps_accuracy": 90.0, "battery_level": 94.0}
```

![Docker](https://github.com/jceloria/docker-http2mqtt/workflows/Docker/badge.svg)
