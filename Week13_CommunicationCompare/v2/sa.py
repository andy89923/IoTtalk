# https://github.com/IoTtalk/Dummy_Device_IoTtalk_v2_py
import random
import time
from iottalkpy.dan import NoData

### The registeration api url, you can use IP or Domain.
# api_url = 'http://localhost:9992'  # default
# api_url = 'http://localhost/csm'  # with URL prefix
# api_url = 'http://localhost:9992/csm'  # with URL prefix + port

api_url = 'https://iottalk2.tw/csm'

### [OPTIONAL] If not given or None, server will auto-generate.
# device_name = 'Dummy_Test'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
# device_addr = "..."

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
# persistent_binding = True

### [OPTIONAL] If not given or None, this device will be used by anyone.
# username = 'myname'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['DummySensor-I']
odf_list = ['DummyControl-O']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 0.1  # global interval
interval = {
    'Dummy_Sensor': 0.1,  # assign feature interval
}

history = []
send_data = 0
start_time = time.perf_counter()

def on_register(dan):
    print('register successfully')


def DummySensor_I():
    global send_data, start_time
    send_data += 1
    start_time = time.perf_counter()
    return send_data


def DummyControl_O(data: list):
    global start_time, send_data

    data = data[0]
    end_time = time.perf_counter()
    history.append(end_time - start_time)
    print('Got', data, history[-1])
    if send_data == 100:
        print('\nAverage Latency =', sum(history) / len(history))