from flask import Flask, request, abort
from flask import render_template
from flask import make_response, send_from_directory

import os
import csmapi

app = Flask(__name__)

@app.route('/RemoteControl/<device_id>/', methods=['GET'])
def remote_control(device_id):

    def register_remote_control(device_id):
        profile = {
            'd_name': device_id,
            'dm_name': 'Remote_control',
            'u_name': 'yb',
            'is_sim': False,
            'df_list': [],
        }            
        try:
            result = csmapi.register(device_id, profile)
            if result: print('Remote control generator: Remote Control successfully registered.')
            return result
        except Exception as e:
            print('Remote control generator: ', e)


    profile = None
    try:
        profile = csmapi.pull(device_id, 'profile')
        print("Device found & connected successfully!")
    except Exception as e:
        print('Remote control generator: ', e)
        if str(e).find('mac_addr not found:') != -1:
            print('Remote control generator: Register Remote Control...')
            result = register_remote_control(device_id)
            return 'Remote control "'+device_id+'" successfully registered. <br> Please bind it in the IoTtalk GUI.', 200
        else:
            print('Remote control generator: I dont know how to handel this error. Sorry...pass.')
            abort(404)
    
    Ctl_O = csmapi.pull(device_id, '__Ctl_O__')
    if Ctl_O != []:
        selected_df_flags = Ctl_O[0][1][1]['cmd_params'][0]
        df_list = profile['df_list']
        df_dict = {'Butt': 0, 'Colo': 0, 'Keyp': 0, 'Knob': 0, 'Swit': 0, 'Togg':0, 'Slid':0}
        for index, element in list(enumerate(selected_df_flags)):
            if element == '1': 
                df_dict[df_list[index][:4]] += 1

    print('Device: ', df_dict)

    return make_response(render_template('remote_control.html', device_id=device_id, df_dict=df_dict))        


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run('0.0.0.0', port=32767, threaded=True, use_reloader=False)