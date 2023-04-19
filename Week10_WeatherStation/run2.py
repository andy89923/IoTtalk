import time, random 
import requests
import threading, sys # for using a Thread to read keyboard INPUT
import DAN
from time import sleep

ServerURL = 'https://3.iottalk.tw/'

Reg_addr = None #if None, Reg_addr = MAC address

mac_addr = 'CD8600D38' + str(1234) 


Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !
DAN.profile['dm_name'] = 'Dummy_Device'                       
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name']  = "CTF." + str(random.randint(100,999 )) + "_" + DAN.profile['dm_name'] # None
DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);

gotInput = False
theInput = "haha"
allDead = False


while True:
    try:
        if(allDead): break;
        value1 = DAN.pull('Dummy_Control')
        if value1 != None:    # 不等於 None 表示有抓到資料
            print (value1[0])
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    try:
       time.sleep(0.2)
    except KeyboardInterrupt:
       break

time.sleep(0.25)
try: 
   DAN.deregister()
except Exception as e:
   print("===")
print("Bye ! --------------", flush=True)
sys.exit( );