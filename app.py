from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is joseph'
   
@app.route('/create', methods=['POST','GET'])
def create():
    if (request.method =='GET'):
         return 'IDINNO_YOLO_Project'
    elif request.method == 'POST':
         params = request.get_json()
         return 'ok'
    else:
         return 'NONE'

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
