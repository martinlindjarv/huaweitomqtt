import time
from huawei_solar import HuaweiSolar
import huawei_solar
import paho.mqtt.client
import os

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

## Inverter parameters from environment - these are defaults if none provided!
inverter_ip = os.getenv('INVERTER_IP', '192.168.1.1')
inverter_port = int(os.getenv('INVERTER_PORT', '6607'))
inverter_slave = int(os.getenv('INVERTER_SLAVE', '0'))

## MQTT parameters from environment and setting defaults here if not provided!
mqtt_host = os.getenv('MQTT_HOST', '192.168.1.1')
mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
mqtt_username = os.getenv('MQTT_USER', 'username')
mqtt_password = os.getenv('MQTT_PASS', 'password')
mqtt_base_topic =  os.getenv('MQTT_BASE_TOPIC', 'solar/NodeHuawei/')


log.info("Connecting to inverter: %s:%s (slave: %s) ", inverter_ip,inverter_port,inverter_slave)
inverter = huawei_solar.HuaweiSolar(inverter_ip, port=inverter_port, slave=inverter_slave )
inverter._slave = inverter_slave 
inverter.wait = 1

## Define vars, so they can be used later
pv01_volt = None
pv01_current = None
pv02_volt = None
pv02_current = None
pv01_power = None
pv02_power = None

accumulated_yield_energy = None
grid_accumulated_energy = None
grid_exported_energy = None
grid_accumulated_energy = None

grid_A_voltage = None
grid_B_voltage = None
grid_C_voltage = None

active_grid_A_current = None
active_grid_B_current = None
active_grid_C_current = None

active_grid_power_factor = None

grid_A_power = None
grid_B_power = None
grid_C_power = None

# parameters to calculate active house consumption in watts
# calculation needs per phase numbers!
# calculation without phases  => house_sum = (storage_charge_discharge_power + (input_power * -1) + power_meter_active_power [sum of active_grid_ABC_power]) * -1
input_power = None
storage_charge_discharge_power = None
active_grid_A_power = None
active_grid_B_power = None
active_grid_C_power = None
power_meter_active_power = None

def modbusAccess():

    # parameters that are taken immidiately
    vars_inmediate = ['pv_01_voltage', 'pv_01_current', 'pv_02_voltage','pv_02_current', 
    'input_power', 'grid_voltage', 
    'grid_current', 'active_power', 
    'grid_A_voltage', 'active_grid_A_current', 'grid_B_voltage', 'active_grid_B_current', 'grid_C_voltage', 'active_grid_C_current', 'power_meter_active_power', 'active_grid_A_power', 'active_grid_B_power', 'active_grid_C_power',
    'storage_charge_discharge_power','storage_state_of_capacity', 'meter_status', 'daily_yield_energy', 'total_yield', 'day_active_power_peak', 'efficiency','active_grid_power_factor', 'power_factor', 
    'grid_exported_energy', 'grid_accumulated_energy', 'device_status', 'fault_code', 'accumulated_yield_energy', 'storage_unit_1_current_day_charge_capacity', 'storage_unit_1_current_day_discharge_capacity', 
    'storage_maximum_charge_power', 'storage_maximum_charging_power'
    ]

    # parameters after approx every 90 seconds
    vars = ['internal_temperature', 'insulation_resistance', 
    'nb_optimizers',  'nb_pv_strings', 'nb_mpp_tracks',
    'storage_working_mode_a', 'storage_total_charge', 'storage_total_discharge', 'storage_unit_1_battery_temperature', 'storage_unit_1_working_mode_b', 'storage_unit_1_running_status', 'storage_unit_1_remaining_charge_dis_charge_time',
    'storage_running_status'
    ]

    cont = 0
    while True:


        for i in vars_inmediate:
            try:
                mid = inverter.get(i)
                log.debug(i)
                log.debug(mid)
                log.debug("---")

                if(isinstance(mid.value, str)):
                  clientMQTT.publish(topic=mqtt_base_topic+i, payload=str(mid.value), qos=1, retain=False)
                if(float(mid.value) < 21474836):
                  clientMQTT.publish(topic=mqtt_base_topic+i, payload=str(mid.value), qos=1, retain=False)

                  # publish to mqtt if battery is charging (true) or not (false)
                  if(i == "storage_charge_discharge_power"):
                    if(mid.value > 0):
                      clientMQTT.publish(topic=mqtt_base_topic+"battery_is_charging", payload="true", qos=1, retain=False)
                    if(mid.value < 0):
                      clientMQTT.publish(topic=mqtt_base_topic+"battery_is_charging", payload="false", qos=1, retain=False)
                    if(mid.value == 0):
                      clientMQTT.publish(topic=mqtt_base_topic+"battery_is_charging", payload="false", qos=1, retain=False)

                  # publish to mqtt if battery charging is (true) or is not (false) allowed
                  if(i == "storage_maximum_charging_power"):
                    if(mid.value > 0):
                      clientMQTT.publish(topic=mqtt_base_topic+"battery_charging_allowed", payload="true", qos=1, retain=False)
                    if(mid.value == 0):
                      clientMQTT.publish(topic=mqtt_base_topic+"battery_charging_allowed", payload="false", qos=1, retain=False)

                  if(i == "pv_01_voltage"):
                    pv01_volt = float(mid.value)
                  if(i == "pv_01_current"):
                    pv01_current = float(mid.value)

                  if(i == "pv_02_voltage"):
                    pv02_volt = float(mid.value)
                  if(i == "pv_02_current"):
                    pv02_current = float(mid.value)

                  if(i == "accumulated_yield_energy"):
                    accumulated_yield_energy = float(mid.value)
                  if(i == "grid_accumulated_energy"):
                    grid_accumulated_energy = float(mid.value)
                  if(i == "grid_exported_energy"):
                    grid_exported_energy = float(mid.value)
                  if(i == "grid_accumulated_energy"):
                    grid_accumulated_energy = float(mid.value)

                  if(i == "grid_A_voltage"):
                    grid_A_voltage = float(mid.value)
                  if(i == "grid_B_voltage"):
                    grid_B_voltage = float(mid.value)
                  if(i == "grid_C_voltage"):
                    grid_C_voltage = float(mid.value)

                  if(i == "active_grid_power_factor"):
                    active_grid_power_factor = float(mid.value)
                  if(i == "power_factor"):
                    power_factor = float(mid.value)

                  if(i == "active_grid_A_current"):
                    active_grid_A_current = float(mid.value)
                  if(i == "active_grid_B_current"):
                    active_grid_B_current = float(mid.value)
                  if(i == "active_grid_C_current"):
                    active_grid_C_current = float(mid.value)

                  if(i == "active_grid_A_power"):
                    active_grid_A_power = float(mid.value)
                  if(i == "active_grid_B_power"):
                    active_grid_B_power = float(mid.value)
                  if(i == "active_grid_C_power"):
                    active_grid_C_power = float(mid.value)


                  if(i == "input_power"):
                    input_power = float(mid.value)
                  if(i == "power_meter_active_power"):
                    power_meter_active_power = float(mid.value)
                  if(i == "storage_charge_discharge_power"):
                    storage_charge_discharge_power = float(mid.value)

            except:
                pass

        if(cont > 5):
            for i in vars:
                try:
                    mid = inverter.get(i)
                    log.debug(i)
                    log.debug(mid)
                    log.debug("---")
                    if(isinstance(mid.value, str)):
                      clientMQTT.publish(topic=mqtt_base_topic+i, payload=str(mid.value), qos=1, retain=False)
                    if(float(mid.value) < 21474836):
                      clientMQTT.publish(topic=mqtt_base_topic+i, payload=str(mid.value), qos=1, retain=False)
                except:
                    pass

            cont = 0

        cont += 1
        time.sleep(5)

        if(accumulated_yield_energy != None and grid_accumulated_energy != None and grid_exported_energy != None):
          # calculate consumption
          consumption = accumulated_yield_energy + grid_accumulated_energy - grid_exported_energy
          clientMQTT.publish(topic=mqtt_base_topic+"consumption", payload=str(consumption), qos=1, retain=False)

        if(grid_accumulated_energy != None):
          self_sufficient_percent = (consumption - grid_accumulated_energy) / consumption * 100
          clientMQTT.publish(topic=mqtt_base_topic+"self_sufficient_percent", payload=str(round(self_sufficient_percent, 1)), qos=1, retain=False)

        if(pv01_volt != None and pv01_current != None):
          pv01_power = pv01_volt * pv01_current
          clientMQTT.publish(topic=mqtt_base_topic+"pv_01_power", payload=str(pv01_power), qos=1, retain=False)

        if(pv02_volt != None and pv02_current != None):
          pv02_power = pv02_volt * pv02_current
          clientMQTT.publish(topic=mqtt_base_topic+"pv_02_power", payload=str(pv02_power), qos=1, retain=False)

        if(pv01_power != None and pv02_power != None):
          pv_power = pv01_power + pv02_power
          clientMQTT.publish(topic=mqtt_base_topic+"pv_power", payload=str(round(pv_power,2)), qos=1, retain=False)

        #<0: supply from the power grid
        if(active_grid_A_power <= 0):
          active_power_phase_A_from_grid = active_grid_A_power * -1
          active_power_phase_A_to_grid = 0 
       #> 0: feed-in to the power grid.
        else:
          active_power_phase_A_to_grid = active_grid_A_power
          active_power_phase_A_from_grid = 0

        #<0: supply from the power grid
        if(active_grid_B_power <= 0):
          active_power_phase_B_from_grid = active_grid_B_power * -1
          active_power_phase_B_to_grid = 0
        #> 0: feed-in to the power grid.
        else:
          active_power_phase_B_to_grid = active_grid_B_power
          active_power_phase_B_from_grid = 0

        #<0: supply from the power grid
        if(active_grid_C_power <= 0):
          active_power_phase_C_from_grid = active_grid_C_power * -1
          active_power_phase_C_to_grid = 0
        #> 0: feed-in to the power grid.
        else:
          active_power_phase_C_to_grid = active_grid_C_power
          active_power_phase_C_from_grid = 0

        ## now lets sum those up and send to mqtt
        active_power_phases_from_grid = round((active_power_phase_A_from_grid + active_power_phase_B_from_grid + active_power_phase_C_from_grid),0)
        active_power_phases_to_grid = round((active_power_phase_A_to_grid + active_power_phase_B_to_grid + active_power_phase_C_to_grid),0)

        # send to MQTT as W
        clientMQTT.publish(topic=mqtt_base_topic+"active_power_phases_from_grid", payload=str(int(active_power_phases_from_grid)), qos=1, retain=False)
        clientMQTT.publish(topic=mqtt_base_topic+"active_power_phases_to_grid", payload=str(int(active_power_phases_to_grid)), qos=1, retain=False)
        # send to mqtt as kW
        clientMQTT.publish(topic=mqtt_base_topic+"active_power_phases_from_grid_kw", payload=str(round(((active_power_phases_from_grid)/1000),3)), qos=1, retain=False)
        clientMQTT.publish(topic=mqtt_base_topic+"active_power_phases_to_grid_kw", payload=str(round(((active_power_phases_to_grid)/1000),3)), qos=1, retain=False)


        if(grid_A_voltage != None and active_grid_A_current != None):
          grid_A_power = grid_A_voltage * active_grid_A_current * power_factor
          clientMQTT.publish(topic=mqtt_base_topic+"grid_A_power", payload=str(round(grid_A_power,3)), qos=1, retain=False)

          # if negative, export to grid and if positive import from grid
          if(grid_A_power <= 0): # export to grid if negative
            grid_A_power_to_grid = grid_A_power * -1
            grid_A_power_from_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_A_power_to_grid", payload=str(round(grid_A_power_to_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_A_power_from_grid", payload=str("0"), qos=1, retain=False)

          else: # import from grid if positive
            grid_A_power_from_grid = grid_A_power
            grid_A_power_to_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_A_power_from_grid", payload=str(round(grid_A_power_from_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_A_power_to_grid", payload=str("0"), qos=1, retain=False)

        if(grid_B_voltage != None and active_grid_B_current != None):
          grid_B_power = grid_A_voltage * active_grid_B_current * power_factor
          clientMQTT.publish(topic=mqtt_base_topic+"grid_B_power", payload=str(round(grid_B_power,3)), qos=1, retain=False)

          # if negative, export to grid and if positive import from grid
          if(grid_B_power <= 0): # export to grid if negative
            grid_B_power_to_grid = grid_B_power * -1
            grid_B_power_from_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_B_power_to_grid", payload=str(round(grid_B_power_to_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_B_power_from_grid", payload=str("0"), qos=1, retain=False)

          else: # import from grid if positive
            grid_B_power_from_grid = grid_B_power
            grid_B_power_to_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_B_power_from_grid", payload=str(round(grid_B_power_from_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_B_power_to_grid", payload=str("0"), qos=1, retain=False)


        if(grid_C_voltage != None and active_grid_C_current != None):
          grid_C_power = grid_C_voltage * active_grid_C_current * power_factor
          clientMQTT.publish(topic=mqtt_base_topic+"grid_C_power", payload=str(round(grid_C_power,3)), qos=1, retain=False)

          # if negative, export to grid and if positive import from grid
          if(grid_C_power <= 0): # export to grid if negative
            grid_C_power_to_grid = grid_C_power * -1
            grid_C_power_from_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_C_power_to_grid", payload=str(round(grid_C_power_to_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_C_power_from_grid", payload=str("0"), qos=1, retain=False)

          else: # import from grid if positive
            grid_C_power_from_grid = grid_C_power
            grid_C_power_to_grid = 0 # define it as zero, so it wouldn't fail later!
            clientMQTT.publish(topic=mqtt_base_topic+"grid_C_power_from_grid", payload=str(round(grid_C_power_from_grid,3)), qos=1, retain=False)
            # lets send power_from_grid as zero
            clientMQTT.publish(topic=mqtt_base_topic+"grid_C_power_to_grid", payload=str("0"), qos=1, retain=False)

        if(active_grid_A_power != None and active_grid_B_power != None and active_grid_C_power != None and input_power != None and storage_charge_discharge_power != None):
          # calculation without phases  => house_sum = (storage_charge_discharge_power + (input_power * -1) + [sum of active_grid_ABC_power]) * -1

          ## summed_phases_consumption on vale, kuna seal on sees ka see kui mingi faas myyb ja mingi ostab!
          ## arvestama peaks ainult positiivsete faasidega ... ?
          summed_phases_consumption = active_grid_A_power + active_grid_B_power + active_grid_C_power
          current_house_consumption = (storage_charge_discharge_power + (input_power * -1) + summed_phases_consumption) * -1
          clientMQTT.publish(topic=mqtt_base_topic+"current_house_consumption_by_phases", payload=str(round((current_house_consumption/1000),3)), qos=1, retain=False)

          # calculate house consumption for each phase
          current_house_consumption_phase_A = (storage_charge_discharge_power/3 + (input_power/3 * -1) + active_grid_A_power) * -1
          clientMQTT.publish(topic=mqtt_base_topic+"current_house_consumption_phase_A", payload=str(round((current_house_consumption_phase_A/1000),3)), qos=1, retain=False)
          current_house_consumption_phase_B = (storage_charge_discharge_power/3 + (input_power/3 * -1) + active_grid_B_power) * -1
          clientMQTT.publish(topic=mqtt_base_topic+"current_house_consumption_phase_B", payload=str(round((current_house_consumption_phase_B/1000),3)), qos=1, retain=False)
          current_house_consumption_phase_C = (storage_charge_discharge_power/3 + (input_power/3 * -1) + active_grid_C_power) * -1
          clientMQTT.publish(topic=mqtt_base_topic+"current_house_consumption_phase_C", payload=str(round((current_house_consumption_phase_C/1000),3)), qos=1, retain=False)


        if(power_meter_active_power != None and input_power != None and storage_charge_discharge_power != None):
          # calculation without phases  => house_sum = (storage_charge_discharge_power + (input_power * -1) + power_meter_active_power) * -1
          input_power_neg = input_power * -1
          current_house_consumption = storage_charge_discharge_power + input_power_neg + power_meter_active_power
          current_house_consumption_neg = current_house_consumption * -1
          clientMQTT.publish(topic=mqtt_base_topic+"current_house_consumption", payload=str(round((current_house_consumption_neg/1000),3)), qos=1, retain=False)

        # sum phases power to and from grid
        grid_phases_power_to_grid_sum_kw = round(((grid_A_power_to_grid + grid_B_power_to_grid + grid_C_power_to_grid)/1000),3)
        clientMQTT.publish(topic=mqtt_base_topic+"grid_phases_power_to_grid_sum_kw", payload=str(grid_phases_power_to_grid_sum_kw), qos=1, retain=False)

        grid_phases_power_from_grid_sum_kw = round(((grid_A_power_from_grid + grid_B_power_from_grid + grid_C_power_from_grid)/1000),3)
        clientMQTT.publish(topic=mqtt_base_topic+"grid_phases_power_from_grid_sum_kw", payload=str(grid_phases_power_from_grid_sum_kw), qos=1, retain=False)




def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        log.info("MQTT OK!")
        clientMQTT.publish(topic=mqtt_base_topic+"LWT", payload="Online", qos=0, retain=True)
        log.info("MQTT base topic: %s", mqtt_base_topic)
    else:
        log.info("MQTT FAILURE. ERROR CODE: %s",rc)
        

paho.mqtt.client.Client.connected_flag=False#create flag in class

clientMQTT = paho.mqtt.client.Client()
clientMQTT.on_connect=on_connect #bind call back function
clientMQTT.loop_start()
log.info("Connecting to MQTT broker: %s:%s ",mqtt_host, mqtt_port)
clientMQTT.username_pw_set(mqtt_username,mqtt_password)
clientMQTT.will_set(mqtt_base_topic+"LWT", payload="Offline", qos=0, retain=True)
clientMQTT.connect(mqtt_host, mqtt_port, 60) #connect to broker
while not clientMQTT.connected_flag: #wait in loop
    log.info("...")
    time.sleep(1)
    pass
time.sleep(1)
log.info("START MODBUS...")

try:
   modbusAccess()
except:
   log.error("Error connecting inverter! Stopping MQTT!")
   clientMQTT.loop_stop()
   exit(1)
