from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is joseph'

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
   
@user_bp.route('/create', methods=['POST'])
def create():
    params = request.get_json()
    return 'ok'
