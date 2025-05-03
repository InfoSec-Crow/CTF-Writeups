#!/usr/bin/python3 
import hashlib
import base64
import sqlite3
import sys

# modified version of: https://github.com/iamaldi/grafana2hashcat

def calculate_hash(password, salt):
    decoded_hash = bytes.fromhex(password)
    salt_base64 = base64.b64encode(salt.encode('utf-8')).decode('utf-8')
    hash_base64 = base64.b64encode(decoded_hash).decode('utf-8')
    return f'sha256:10000:{salt_base64}:{hash_base64}'

def read_db():
    db_path = sys.argv[1]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT login,password,salt FROM user")
    rows = cursor.fetchall()
    conn.close()
    return rows

def to_hash():
    data = read_db()
    for data in read_db():
        name = data[0]
        password = data[1]
        salt = data[2]
        hashcat = calculate_hash(password, salt)
        print(f'[+] Got hash for user {name}, save it in {name}_hash.txt')
        with open(f'{name}_hash.txt', 'w') as file:
            file.write(hashcat)

to_hash()
print('\nHashcat command:\nhashcat -m 10900 name_hash.txt /usr/share/wordlists/rockyou.txt')
