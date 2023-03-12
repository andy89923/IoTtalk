import time, random 
import requests
import threading, sys
import DAN

ServerURL = 'https://3.iottalk.tw/'

Reg_addr = None

mac_addr = 'CD8600D38' + '0000'

Reg_addr = mac_addr
DAN.profile['dm_name'] = 'Dummy_Device'

DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']   # Check IoTtalk to see what IDF/ODF the DM has

DAN.profile['d_name']  = "CTF.0" + "_" + DAN.profile['dm_name']

DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);

gotInput = False
theInput = "haha"
allDead = False

def doRead( ):
    global gotInput, theInput, allDead
    while True:   
        while gotInput:   # 老闆還沒把資料拿走
           time.sleep(0.1)    # 小睡 下把 CPU 暫時讓給別人
           continue  # go back to while   
        try:     # 準備讀取資料, 注意程式會卡在這等 User 輸入, 所以要用 Thread
           theInput = input("Give me data: ")
        except Exception:    ##  KeyboardInterrupt:
           allDead = True
           print("\n\nDeregister " + DAN.profile['d_name'] + " !!!\n",  flush=True)
           DAN.deregister()
           sys.stdout = sys.__stdout__
           print(" Thread say Bye bye ---------------", flush=True)
           sys.exit( );   ## break  # raise   #  ?
        if theInput =='quit' or theInput == "exit":    # these are NOT data
           allDead = True
        else:
           print("Will send " + theInput, end="   , ")
           gotInput=True   # notify my master that we have data 
        if allDead: break;   # 離開 while True 這 Loop  

#creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw 
threadx = threading.Thread(target=doRead)
threadx.daemon = True  # 這樣才不會阻礙到主程式的結束
threadx.start()

while True:
    try:
        if(allDead): break;
        value1=DAN.pull('Dummy_Control')
        if value1 != None:    # 不等於 None 表示有抓到資料
            print (value1[0])
        if gotInput:
           try:
              value2=float( theInput )   # 故意轉成實數 
           except:
              value2=0 
           if(allDead): break;
           gotInput=False
           DAN.push ('Dummy_Sensor', value2,  value2) 

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
   DAN.deregister()    # 試著解除註冊
except Exception as e:
   print("===")
print("Bye ! --------------", flush=True)
sys.exit( );