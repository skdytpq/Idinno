from flask import Flask, request, jsonify
import os
import time
from PIL import Image
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Idinnolab'
   
@app.route('/create', methods=['POST','GET'])
def create():
    if (request.method =='GET'):
         return 'IDINNO_YOLO_Project'
    elif request.method == 'POST':
         params = request.get_json()
         img_id = params['pInfo'][0]['img_id']
         #os.system("curl " + img_url + " > test.jpg")
         if img_id == 'C01':
            return 'p_of_sa_m_10_0001 '
         elif img_id == 'C02':
            return 'p_of_sa_w_10_0001'
         elif img_id == 'C03':
             return 'p_of_sa_w_30_0001'
         elif img_id == 'C04':
            return 'p_of_sa_w_30_0002'
         else: 
            return 'p_of_sa_w_30_0002'
    else:
         return 'NONE'

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
