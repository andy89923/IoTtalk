import time, random 
import threading, sys # for using a Thread to read keyboard INPUT
import DAN
from time import sleep

ServerURL = 'https://3.iottalk.tw/'

Reg_addr = None #if None, Reg_addr = MAC address

mac_addr = 'CD8600D38' + str(3458) 


# Note that the mac_addr generated in DAN.py always be the same cause using UUID !
Reg_addr = mac_addr
DAN.profile['dm_name'] = 'CTF_Dummy_153'                       
DAN.profile['d_name']  = DAN.profile['dm_name'] + "_O2"
DAN.profile['df_list'] = ['Color-I', 'slider', 'Dummy_Control', 'Dmy_t153']
DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name'])
print("Server is ", ServerURL);

gotInput = False
theInput = "haha"
allDead = False

while True:
    try:
        if(allDead): break;

        value2 = DAN.pull('Dmy_t153')
        if value2 != None: print('Dmy_t153', value2[0])

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