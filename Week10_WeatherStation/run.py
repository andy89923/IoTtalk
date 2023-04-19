import time, random 
import requests
import threading, sys # for using a Thread to read keyboard INPUT
import DAN
from crawler import getWeatherData
from time import sleep

ServerURL = 'https://3.iottalk.tw/'

Reg_addr = None #if None, Reg_addr = MAC address

mac_addr = 'CD8600D38' + str(3456) 


Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !
DAN.profile['dm_name'] = 'CTF_WS'                       
DAN.profile['df_list'] = ['.HUMD', '.H_24R', '.PRES', '.TEMP']
DAN.profile['d_name']  = DAN.profile['dm_name']
DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);

gotInput = False
theInput = "haha"
allDead = False

def doRead( ):
    global gotInput, theInput, allDead
    while True:   
        while gotInput:
           time.sleep(0.1)
           continue
        try:
           theInput = getWeatherData()
        except Exception:
           allDead = True
           print("\n\nDeregister " + DAN.profile['d_name'] + " !!!\n",  flush=True)
           DAN.deregister()
           sys.stdout = sys.__stdout__
           print(" Thread say Bye bye ---------------", flush=True)
           sys.exit( );
        if theInput =='quit' or theInput == "exit":    # these are NOT data
           allDead = True
        else:
           gotInput = True
        sleep(10)
        if allDead: break;


#creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw 
threadx = threading.Thread(target = doRead)
threadx.daemon = True  # 這樣才不會阻礙到主程式的結束
threadx.start()


while True:
    try:
        if(allDead): break;
        # value1 = DAN.pull('.Output')
        # if value1 != None:    # 不等於 None 表示有抓到資料
        #     print (value1[0])
        # Push data to a device feature called "Dummy_Sensor" 
        if gotInput:  # 小弟有讀到資料了 
           # we have data in theInput
           if(allDead): break;
           gotInput = False    
           DAN.push('.TEMP', f'TEMP {theInput[0]}', f'TEMP {theInput[0]}')
           sleep(0.5)
           DAN.push('.HUMD', f'HUMD {theInput[1]}', f'HUMD {theInput[1]}')
           sleep(0.5)
           DAN.push('.PRES', f'PRES {theInput[2]}', f'PRES {theInput[2]}')
           sleep(0.5)
           DAN.push('.H_24R', f'H_24R {theInput[3]}', f'H_24R {theInput[3]}')


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