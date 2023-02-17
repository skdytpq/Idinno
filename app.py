from flask import Flask, request, jsonify
import os
import time
from PIL import Image
from yolov5.detect import main1  
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Idinnolab'
   
@app.route('/create', methods=['POST','GET'])
def create():
    if (request.method =='GET'):
         r = main1(source = 'https://ethno-mining.com/resources/persona/curation/230201/2302011128.jpg')
         print(main1)
         return 'IDINNO_YOLO_Project',r
    elif request.method == 'POST':
         params = request.get_json()
         img_id = params['pInfo'][0]['img_id']
         #os.system("curl " + img_url + " > test.jpg")
         rr = main1(source = img_id)
         for i in range(len(rr)):
            return i

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
   
