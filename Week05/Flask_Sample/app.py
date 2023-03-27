from flask import Flask, request, abort
from flask import render_template
from flask import make_response

import csmapi

app = Flask(__name__)

@app.route('/<device_id>/<count>/', methods=['GET'])
def switch_generator(device_id, count):

    sync = request.args.get('sync')
    if sync != 'True': sync = False

    def register_remote_control(device_id):
        profile = {
            'd_name': device_id,
            'dm_name': 'Remote_control',
            'u_name': 'yb',
            'is_sim': False,
            'df_list': [],
        }
        for i in range(1,26):
            profile['df_list'].append("Switch%d" % i)
            
        try:
            result = csmapi.register(device_id, profile)
            if result: print('Remote control generator: Remote Control successfully registered.')
            return result
        except Exception as e:
            print('Remote control generator: ', e)

    profile = None
    try:
        profile = csmapi.pull(device_id, 'profile')
    except Exception as e:
        print('Remote control generator: ', e)
        if str(e).find('mac_addr not found:') != -1:
            print('Remote control generator: Register Remote Control...')
            result = register_remote_control(device_id)
            return 'Remote control "'+device_id+'" successfully registered. <br> Please bind it in the IoTtalk GUI.', 200
        else:
            print('Remote control generator: I dont know how to handel this error. Sorry...pass.')
            abort(404)

    df_dict = {'Swit': 0}        
    df_dict['Swit']= int(count)
    return make_response(render_template('switch.html', device_id=device_id, df_dict=df_dict, sync=sync))        

if __name__ == "__main__":
    app.run('0.0.0.0', port=32767, threaded=True, use_reloader=False)