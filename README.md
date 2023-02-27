# huaweitomqtt

Get Huawei ModBusTCP data and send it to MQTT

Based on script from https://github.com/ccorderor/huawei-sun2000-modbus-mqtt

Things needed:
- Enable Modbus in inverter (NB! installer account needed) _OR install separate GW for modbus to connect directly to inverter wifi!_
  - Settings -> Communication configuration -> Dongle parameter settings -> Modbus-TCP
  - 3 choices: 
     - Disable
     - Enable (restricted) [available to 1 IP address]
     - Enable (unrestricted) [available to same subnet]
- VM in same Subnet
- python3 installed
- pip installed
- download files from this repo
- install requirements: 'pip3 install -r requirements.txt'
- create settings file to /etc/huaweitomqtt/settings.conf with content:
````
# Config file for service huawetomqtt!
INVERTER_IP=192.168.1.1
INVERTER_PORT=6607 #default:6607, can be set to 502
INVERTER_SLAVE=0 #default: 0

MQTT_HOST=192.168.1.2
MQTT_PORT=1883
MQTT_USER=username
MQTT_PASS=password
````
- create systemd service /lib/systemd/system/huaweitomqtt.service

