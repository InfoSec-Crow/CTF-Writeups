#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup, Comment
import re
import time
import sys 

S = requests.Session()

def register():
    data = {
        'name': 'test',
        'username': 'test',
        'password': 'test',
        'addressLine1': 'test',
        'addressLine2': 'test',
        'town': 'test',
        'postcode': '123',
    }
    requests.post('http://bookworm.htb/register', data=data, verify=False)

def login():
    data = {
        'username': 'test',
        'password': 'test',
    }
    S.post('http://bookworm.htb/login', data=data, verify=False)

def write_to_log(text):
    with open('recent_updates.log', 'a') as file:
        with open('recent_updates.log', 'r') as check_file:
            lines = check_file.readlines()
            if text + '\n' not in lines: 
                file.write(text + '\n')

def recent_updates():
    try:
        while True:
            sys.stdout.write('\r' + ' ' * 80)
            sys.stdout.flush()

            text = ''
            r = S.get('http://bookworm.htb/shop', verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for entry in soup.find_all("div", class_="row mb-2"):
                comment = entry.find(string=lambda text: isinstance(text, Comment))
                number = re.search(r'\d+', comment).group() if comment else None
                name_tag = entry.find('strong')
                name = name_tag.get_text(strip=True) if name_tag else None
                text_entry = f'{name} : {number} | '
                text += text_entry
                write_to_log(text_entry)
            sys.stdout.write('\r' + text)
            sys.stdout.flush()
            time.sleep(5)
    except KeyboardInterrupt:
        print('\nExit')

register()
login()
recent_updates()
