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
         opt = parse_opt('https://ethno-mining.com/resources/persona/curation/230201/2302011128.jpg','H')
         rr = main1(opt)
         val = mapping(rr,'H')
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
             return f'{",".join(val)}'
         else:
             opt = parse_opt(img_id,'F')
             r = main1(opt)
             val = mapping(r,'F')
             return f'{",".join(val)}'
      except:
         return 'NaN'  

def mapping(r,tp) :
   person = ['person']

   elec = ['cell phone', 'laptop', 'mouse', 'remote', 'keyboard',  'hair drier', 'toothbrush']

   fur = ['chair', 'couch', 'bed', 'dining table', 'toilet']

   mot = ['bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat']

   inter = ['frisbee', 'kite', 'skis', 'snowboard', 'surfboard', 'tennis racket', 'potted plant', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'baseball bat', 'baseball glove', 'skateboard','sports ball', 'clock', 'vase', 'scissors', 'teddy bear', 'book']

   dish = ['bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl']

   etc = ['fire hydrant', 'stop sign', 'traffic light', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake']


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
      n = {'person' : 0 , 'elec' : 0 , 'fur' : 0 ,'mot' : 0 , 'inter' : 0 , 'dish' : 0 ,'etc' : 0}
      for i in r:
         if i in person:
            n['person'] +=1
         elif i in elec:
            n['elec'] +=1
         elif i in fur:
            n['fur'] +=1
         elif i in mot:
            n['mot'] +=1
         elif i in inter:
            n['inter'] +=1
         elif i in dish:
            n['dish'] +=1
         else:
            n['etc'] +=1
      area = (n['fur']  + n['mot'] + n['inter'] + n['dish'] + n['etc'])/5 # 면적 당 가구 배치
      interior =  int(n['inter']) # 인테리어 요소 배치
      tv_conv = int(n['elec']) # TV 및 편의 요소 배치
      people_conv = int(n['person']) # 편의 요소 대비 사람의 수
      furniture = int(n['fur']) # 가구 대비 사람의 수
      df1 = pd.read_excel('sheet2.xlsx')
      df1 = df1.drop_duplicates(subset = ['persona_no'])
      df1 = df1.reset_index()
      df = pd.read_excel('sheet1.xlsx')
      df = df.rename(columns=df.iloc[0]).iloc[1:,:]
      data  = pd.concat([df1,df],axis = 1)
      score = []
      personas = dict()
      for i in range(data.shape[0]-1):
         td = data.iloc[i,:]
         IE = float(td['내향/외향'])
         SN = float(td['감각/직관'])
         JP = float(td['판단/인식'])
         Trend = float(td['트랜드\n민감도'])
         Quality = float(td['상품/서비스품질'])
         Easy = float(td['이용편의성'][1])
         Age = float(td['age_gender'][:2])
         area_score = area_f(SN, JP, area)
         interior_score = interior_f(Trend, Easy, interior)
         tv_conv_score = tv_conv_f(Easy, tv_conv)
         people_conv_score = people_conv_f(IE, Easy, people_conv)
         furniture_score = furniture_f(IE, Age, furniture)
         total_score = area_score + interior_score + tv_conv_score + people_conv_score + furniture_score
         score.append(total_score)
       a = np.argmax(np.array(score))
       personas[td['persona_no']] = total_score
       res = data.iloc[a,:]['persona_no']
      #persona = pd.DataFrame(personas)
      #persona = persona.rename(columns = {0 : 'score'})
      #persona = persona.sort_values(ascending = False,by = 'score').iloc[:3].index
      #per = np.argmax(np.array(score))
      #persona =data['persona_no'][per]
      return res#persona

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True,threaded=False)
