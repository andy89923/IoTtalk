import time, DAN, requests, random 
import threading, sys
from tkinter import *


ServerURL = 'https://3.iottalk.tw'

tk = Tk()
tk.title("CTF_Dummy_153")
text_widget = Text(tk, height=2, width=36, font=("Simsun", 24), fg="red", bg="lightgreen"); 
text_widget.pack( ); 
text_widget.insert(END, "拉到滿意的值然後放掉滑鼠!")

gotSlider=False
sliderVal = 58  # initVal for the Slider
firstSetSlider=True  # 在一開始 .set(58) 設定 Slider故意不處理 # 已改用滑鼠放掉, 此變數沒用了
def syy_changed(event): 
    global gotSlider, sliderVal  #用來和原先的老大溝通 
    sliderVal=s.get()
    gotSlider=True

s = Scale(tk, from_=0, to=100, length=600, tickinterval=10, bg="lightyellow", fg="red", orient=HORIZONTAL)

# Connect the slider to the callback function
s.bind("<ButtonRelease-1>", syy_changed)  # 滑鼠放掉才算
s.set(sliderVal); s.pack()  # 如果 command 寫在 Scale( ... 那句, 則這 s.set( ) 也會執行它

def kill_me():
    global allDead  # 用來通知 thread 自殺
    allDead=True  #通知所有 thread 自殺
    tk.focus_set()
    sayBye( )
    tk.quit()  # close Tk window

button = Button(tk, text="Quit 點這結束程式", anchor="w",
  bg="yellow", fg="green", command=kill_me)
button.pack(side='right')
tk.protocol("WM_DELETE_WINDOW", kill_me)

Reg_addr = None
mac_addr = 'C9870D238' + str(44)
Reg_addr = mac_addr


DAN.profile['dm_name'] = 'CTF_Dummy_153'
DAN.profile['df_list'] = ['Color-I', 'slider', 'Dummy_Control', 'Dmy_t153']


def initIoTtalk( ):
    DAN.profile['d_name'] = DAN.profile['dm_name'] + "_I"
    DAN.device_registration_with_retry(ServerURL, Reg_addr) 
    print("dm_name is ", DAN.profile['dm_name'])
    print("Server is ", ServerURL);



theInput = "haha"
gotInput = allDead = False
firstRead = True

def doRead( ):
    global gotInput, theInput, allDead, firstRead
    while True:
        if(allDead): break
        if gotInput:
           time.sleep(0.1)
           continue  # go back to while
        try:
           if firstRead:
              print("提醒輸入 quit 會結束 !")  #只在第一次輸入之前才提醒
              firstRead=False
           theInput = input("Give me data: ")
        except KeyboardInterrupt:
           allDead = True
           break
        except Exception:    ##  KeyboardInterrupt:
           allDead = True
           sys.stdout = sys.__stdout__
           print(" Thread say Bye bye ---------------", flush=True)
           break  # raise   #  sys.exit(0);   ## break  # raise   #  ?
        gotInput=True
        if(allDead): kill_me( )
        elif theInput !='quit' and theInput != "exit":
           print("Will send " + theInput, end="   , ")

#creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw
threadx = threading.Thread(target=doRead)
threadx.daemon = True

def doDummy( ):  # 因為 Tkinter  必須在 main thread, 所以原先的主程式必須改用 thread (thready)
  global gotInput, theInput, allDead  # do NOT forget these var should be global
  global gotSlider, firstSetSlider  # 沒寫  sliderVal = xxx 就不必寫 global 
  while True:
    if(allDead): break
    try:
        value1=DAN.pull('Dummy_Control')
        if value1 != None:
            print (value1[0])
        if gotSlider:  # Slider 有被動到
           sss = sliderVal  # 取出 slider value
           gotSlider = False #其實沒用處, 因為我們不管 user 是否會去改變  Slider
           if firstSetSlider:
              firstSetSlider=False
              DAN.push ('slider', 100);  time.sleep(0.2)  # 怕燈泡來不及收取
              DAN.push ('slider', 0);  time.sleep(0.2) # 這時 DAI6.py 收不到這兩個喔 ! 想想why?
              print ("Slider 第一次的值: ", sss)  # 可在第一次故意先送 100, 再送 0, 再送 sss
              DAN.push ('slider', sss)  # 若不送就把這列註解掉
              pass    # 第一次是我們 .set( ) 的, 故意不處理; # 現改check滑鼠放掉不會查到  .set(58)
           else:  # 不是我們一開始 .set( )的 !
              print ("Slider 被拉到 ", sss)  # 可以用  DAN.push( ) 送去 IoTtalk server
              DAN.push ('slider', sss)
        #end of if gotSlider
        if gotInput:
           if theInput =='quit' or theInput=="exit":
              allDead = True
              break;  #  sys.exit( );
           # value2=random.uniform(1, 10)

           c = 'l'
           try:
              datas = theInput.split(' ')
              c = datas[0]
              value2=float(theInput)
           except:
              value2=0
           gotInput=False   # so that you can input again 
           if(allDead): break;
           
           if c == 'l': DAN.push('slider', int(datas[1]))
           if c == 'c': DAN.push('Color-I', int(datas[1]), int(datas[2]), int(datas[3]))

        #end of if gotInput
    except KeyboardInterrupt:
        allDead = True
        break;  # sys.exit( );
    except Exception as e:
        print("allDead: ", allDead)
        if(allDead):
            break  #  do NOT try to re-register !
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr IS not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    if(allDead): break
    try:
       time.sleep(0.1)  # was 0.2
    except KeyboardInterrupt:
       break
  print("=== end of thready")
  time.sleep(0.015)
  kill_me( );
  sys.exit(0);

def sayBye( ):
  try: 
     time.sleep(0.025)
     DAN.deregister()
  except Exception as e:
     print("===De-Reg Error")
  print("Bye ! --------------", flush=True)
  # sys.exit(0);


# 以下三列把 doDummy 包成 thready 然後叫它平行啟動
thready = threading.Thread(target = doDummy)
thready.daemon = True

if __name__ == '__main__':
   initIoTtalk( )
   threadx.start()
   thready.start()
   tk.mainloop() 