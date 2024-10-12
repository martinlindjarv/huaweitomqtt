# huawei2mqtt

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
- create settings file to /etc/huawei2mqtt/settings.conf with content (default values):
````
# Config file for service huawetomqtt!
INVERTER_IP=192.168.1.1
INVERTER_PORT=6607 
INVERTER_SLAVE=0 

MQTT_HOST=192.168.1.2
MQTT_PORT=1883
MQTT_USER=username
MQTT_PASS=password
MQTT_BASE_TOPIC='solar/NodeHuawei/'
````
- create systemd service /lib/systemd/system/huawei2mqtt.service

