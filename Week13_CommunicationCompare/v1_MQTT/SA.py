import random 
import time

ServerURL = 'https://3.iottalk.tw/'
MQTT_broker = '3.iottalk.tw'
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
device_id = 'Dummy_Device'
device_name = 'CTF_DD'
exec_interval = 0.1

history = []
send_data = 0
start_time = time.perf_counter()

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def Dummy_Sensor():
    global send_data, start_time
    send_data += 1
    start_time = time.perf_counter()
    return send_data

def Dummy_Control(data:list):
    global start_time, send_data

    data = data[0]
    end_time = time.perf_counter()
    history.append(end_time - start_time)
    print('Got', data, history[-1])
    if send_data == 100:
        print('\nAverage Latency =', sum(history) / len(history))
