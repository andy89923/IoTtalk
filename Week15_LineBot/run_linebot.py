from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import DAN
import threading
import time

line_bot_api = LineBotApi('...')
handler = WebhookHandler('...')
user_id_set=set()
app = Flask(__name__)


ServerURL = 'https://3.iottalk.tw/'
Reg_addr = None
mac_addr = 'CD8601D38' + str(5634) 

Reg_addr = mac_addr
DAN.profile['dm_name'] = 'CTF_Line'                       
DAN.profile['df_list'] = ['MSG-I', 'MSG-O']
DAN.profile['d_name']  = DAN.profile['dm_name']
DAN.device_registration_with_retry(ServerURL, Reg_addr) 

print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);

def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))

    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # Reply API example
    DAN.push('MSG-I', Msg)
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)


def pull_odf():
    while True:
        data = DAN.pull('MSG-O')
        if data:
            for userId in user_id_set:
                line_bot_api.push_message(userId, TextSendMessage(text = data[0]))
                user_id_set.remove(userId)
                break
        time.sleep(1)

   
if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
    
    thread = threading.Thread(target=pull_odf)
    thread.daemon = True
    thread.start()
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

