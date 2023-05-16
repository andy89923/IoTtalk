import time, random 
import requests
import threading, sys
import DAN
from time import sleep

ServerURL = 'https://3.iottalk.tw/'

Reg_addr = None
mac_addr = 'CD8600D38' + str(1111) 

Reg_addr = mac_addr
DAN.profile['dm_name'] = 'Dummy_Device'                       
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name']  = 'CTF_DD'
DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name'])
print("Server is ", ServerURL);

time.sleep(10)
print("Start")

send_data = 0
history = []

while True:
   if send_data == 100: break
   start_time = time.perf_counter()
   DAN.push('Dummy_Sensor', send_data)
   try:
     value = DAN.pull('Dummy_Control')
     if value != None:
         end_time = time.perf_counter()
         history.append(end_time - start_time)
         print('Got', value[0], history[-1])
         send_data += 1
   except Exception as e:
      print(e)
      if str(e).find('mac_addr not found:') != -1:
         print('Reg_addr is not found. Try to re-register...')
         DAN.device_registration_with_retry(ServerURL, Reg_addr)
      else:
         print('Connection failed due to unknow reasons.')
         time.sleep(1)

time.sleep(0.25)
try: 
   DAN.deregister()
except Exception as e:
   print("===")


print('\nAverage Latency =', sum(history) / len(history))


print("Bye ! --------------", flush=True)
sys.exit( );