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
         img_id = params['imgUrl']
         os.system("curl " + img_url + " > test.jpg")
         print(params)
         if img_id == '제품중심_사진':
            return '제품중심 사진'
         elif img_id == '제품포함_사진':
            return '제품포함 사진'
         elif img_id == '2D_디자인':
             return '2D_디자인'
         elif img_id == '라인중심_스케치':
            return '라인 스케치'
         return 'ok'
    else:
         return 'NONE'

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
