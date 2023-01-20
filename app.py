from flask import Flask, request, jsonify
import os
import time
from PIL import Image
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is joseph'
   
@app.route('/create', methods=['POST','GET'])
def create():
    if (request.method =='GET'):
         return 'IDINNO_YOLO_Project'
    elif request.method == 'POST':
         start = time.time()
         params = request.get_json()
         img_url = params['imgUrl']
         os.system("curl " + url + " > test.jpg")
         return 'ok'
    else:
         return 'NONE'

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
