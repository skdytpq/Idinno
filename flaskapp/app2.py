from flask import Flask, render_template, request, Response
from flask import request, jsonify
from flask import Response
import os 
import openai
import argparse
import pandas as pd
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
openai.api_key = "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"


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def send_messages(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
def get_response_openai(prompt):
    try:
        prompt = prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            n=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
        
                {"role": "user", "content": prompt},
            ], 
            stream = True
        )
    except Exception as e:
        print("Error in creating campaigns from openAI:", str(e))
        yield 'Error'
        return 503
    try:
        for chunk in response:
            cur_res = chunk['choices'][0]['delta'].get('content',"")
            yield f"data: {cur_res}\n\n"
    except:
        print('Loading Error')
def ok_response():
    return 'ok'
@app.route("/")
def index():
    user_id = 12345  # 실제 사용자 ID라 가정
    response = make_response(render_template('index.html'))  # index.html 렌더링
    # 쿠키 설정
    response.set_cookie('user_session', value=str(user_id), samesite='Strict', secure=True)

    return response
    #return render_template('index.html')
@app.route('/sse', methods=['POST','GET'])
def response():
    if request.method == 'GET':
        prompt = "브랜드에 민감하고, 가격은 중요하지 않으며, 서비스를 중요시여기는 20대 남성페르소나의 노트북 구매 시나리오를 구입전, 구입과정, 이용 후 평가를 기반으로 맥락적으로 작성해줘"
        return Response(get_response_openai(prompt), mimetype='text/event-stream')
#    if request.method == 'GET': 
#        dynamic_data = []
#        prompt = "브랜드에 민감하고, 가격은 중요하지 않으며, 서비스를 중요시여기는 20대 남성페르소나의 노트북 구매 시나리오를 구입전, 구입과정, 이용 후 평가를 기반으로 맥락적으로 작성해줘"
#        response = Response(get_response_openai(prompt), mimetype='text/event-stream')
#        response.set_cookie('JSESSIONID', value='skdytpq98', samesite='None', secure=False)
#        response = make_response(response)
#        return response
        
    elif request.method == 'POST': 
        params = request.get_json()
        age = params['gptInfo'][0]['age']
        #key1 = params['gptInfo'][0]['token']
        key1 = params['gptInfo'][0]['keyword1']
        key2 = params['gptInfo'][0]['keyword2']
        key3 = params['gptInfo'][0]['keyword3']
        key4 = params['gptInfo'][0]['keyword4']
        prompt = f'성격 유형과 일반적인 소비 성향은  "{key2}" 이고, 1개월 기준의 소비 지출 패턴은 "f{key3}" 이며, 최종적인 소비를 결정하는 데 영향을 주는 요인은 "{key4}" 인 {age} 고객이 있어. 이 고객의 {key1} 상품에 대한 사용자 시나리오를 ""안에 키워드를 기반으로 만들어줘 '
    # index.html 파일을 렌더링할 때 데이터를 함께 넘겨줍니다.
        return Response(get_response_openai(prompt), mimetype='text/event-stream')
@app.route("/gpt_ex")
def hello_world():
    prompt = '성격유형과 일반적인 소비 성향은 "할인 혜택 알림 서비스를 이용하며, 서비스를 이용할 때 불편함이 없기를 원합니다." 이고 1개월 소비 지출 패턴은 "한달간 평균 지출하는 비용은 1,322,526원으로서 비슷한 연령에 비하여 15% 많은 수준입니다." 이고 최종적인 소비에 영향을 주는 요인은 "본인 스스로에게는 브랜드 파워요인이 가장 중요하고, 동일한 연령과 성별의 소비자 유형과 비교해 보면   브랜드 파워에 가장 민감한 편입니다." 인 30대 여성 고객이 있어. 이 고객의 온라인 교육 관련 상품에 대한 사용자 시나리오를 ""안에 들어간 키워드를 기반으로 만들어줘'
    response = get_completion(prompt)
    dynamic_data = response
    return render_template('index.html', dynamic_data=dynamic_data)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5001, debug=True,threaded=False)