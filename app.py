from flask import Flask, request, jsonify
import os
import time
from PIL import Image
from yolov5.detect import main1  
import argparse
import pandas as pd
from person import area_f ,interior_f,tv_conv_f,people_conv_f,furniture_f
import numpy as np
app = Flask(__name__)

def parse_opt(img_id,type):
    parser = argparse.ArgumentParser()
    if type == 'F':
      df = 'yolov5/best.pt'
    else: 
      df = 'yolov5/yolov5s_.pt'
    parser.add_argument('--weights', nargs='+', type=str, default= df, help='model path or triton URL')
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
         if params['pInfo'][0]['img_info'] == 'H':
             opt = parse_opt(img_id,'H')
             r = main1(opt)
             val = mapping(r,'H')
             return val
         else:
             opt = parse_opt(img_id,'F')
             r = main1(opt)
             val = mapping(r,'F')
             return f'{",".join(val)}'
      except:
         return 'NaN'

def mapping(r,tp) :
   if tp == 'F':
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
   else :
      area = 20 # 면적 당 가구 배치
      interior = 20 # 인테리어 요소 배치
      tv_conv = 20 # TV 및 편의 요소 배치
      people_conv = 20 # 편의 요소 대비 사람의 수
      furniture = 20 # 가구 대비 사람의 수
      df1 = pd.read_excel('per_1.xlsx', sheet_name=2)
      df1 = df1.drop_duplicates(subset = ['persona_no'])
      df1 = df1.reset_index()
      df = pd.read_excel('per_1.xlsx', sheet_name=3)
      data  = pd.concat([df1,df],axis = 1)
      score = []
      for i in range(data.shape[0]):
         td = data.iloc[i,:]
         IE = td['내향/외향']
         SN = td['감각/직관']
         JP = td['판단/인식']
         Trend = td['트렌드\n민감도']
         Quality = td['상품/서비스품질']
         Easy = td['이용편의성'].iloc[:,0]
         Age = int(td['age_gender'][:2])
         area_score = area_f(SN, JP, area)
         interior_score = interior_f(Trend, Easy, interior)
         tv_conv_score = tv_conv_f(Easy, tv_conv)
         people_conv_score = people_conv_f(IE, Easy, people_conv)
         furniture_score = furniture_f(IE, Age, furniture)
         total_score = area_score + interior_score + tv_conv_score + people_conv_score + furniture_score
         score.appned(total_score)
      per = np.argmax(np.array(score))
      persona =data['persona_no'][per]
      return persona

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True,threaded=False)
