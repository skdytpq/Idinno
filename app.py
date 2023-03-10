from flask import Flask, request, jsonify
import os
import time
from PIL import Image
from yolov5.detect import main1  
import argparse
import pandas as pd

app = Flask(__name__)

def parse_opt(img_id):
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default= 'yolov5/best.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=img_id, help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default='data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default= 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    return opt

@app.route('/')
def home():
   return 'This is Idinnolab'

@app.route('/create', methods=['POST','GET'])
def create():
    if (request.method =='GET'):
         opt = parse_opt('https://ethno-mining.com/resources/persona/curation/230201/2302011128.jpg')
         rr = main1(opt)
         val = mapping(rr)
         return f'{",".join(val)}'
    elif (request.method == 'POST'):
      try:
         params = request.get_json()
         img_id = params["pInfo"][0]["imgUrl"]
         #os.system("curl " + img_url + " > test.jpg")
         opt = parse_opt(img_id)
         r = main1(opt)
         val = mapping(r)
         return f'{",".join(val)}'
      except:
         return 'NaN'

def mapping(r) :
   df = pd.read_excel('per.xlsx')
   val = []
   for i in range(len(df['class'].values)):
      val.append(df['class'].values[i].split(':')[1].strip()[1:-1])
   df['class'] = val
   df.fillna(0,inplace = True)
   get = dict()
   sub_list = []
   for i in df['class'].values:
      for j in df.loc[df['class'] == i].values[0][1:]:
         if j != 0:
               sub_list.append(j)
      get[i] = sub_list
      sub_list = []
   key_list = []
   for key in r:
      key_list.extend(get[key])
   try:
      val = pd.Series(key_list).value_counts().index[0:5]
   except:
      val = pd.Series(key_list).value_counts().index[0:-1]
   return val

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True,threaded=False)