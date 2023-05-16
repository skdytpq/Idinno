
ID = 12 # Image ID
area = 20 # 면적 당 가구 배치
interior = 20 # 인테리어 요소 배치
tv_conv = 20 # TV 및 편의 요소 배치
people_conv = 20 # 편의 요소 대비 사람의 수
furniture = 20 # 가구 대비 사람의 수


IE = float(input('내향/외향 점수 : '))
SN = float(input('감각/직관 점수 : '))
JP = float(input('판단/인식 점수 : '))
Trend = float(input('트렌드민감도 점수 : '))
Quality = float(input('상품/서비스 품질 : '))
Easy = float(input('이용편의성 : '))
Age = int(input('나이대 : '))



def area_f(x, y, z): # x = SN, y = JP, z = area
    x_score = 0
    y_score = 0
    if 0.1 <= x and x <= 1.0:
        x_score = 30
    elif 1.1 <= x and x <= 2.0:
        x_score = 25
    elif 2.1 <= x and x <= 3.0:
        x_score = 20
    elif 3.1 <= x and x <= 4.0:
        x_score = 15
    elif 4.1 <= x and x <= 5.0:
        x_score = 10
    result_x = x_score + z
    
    if 0.1 <= y and y <= 1.0:
        y_score = 30
    elif 1.1 <= y and y <= 2.0:
        y_score = 25
    elif 2.1 <= y and y <= 3.0:
        y_score = 20
    elif 3.1 <= y and y <= 4.0:
        y_score = 15
    elif 4.1 <= y and y <= 5.0:
        y_score = 10
    result_y = y_score + z
    
    result = result_x + result_y
    return result
def interior_f(x, y ,z): # x = Trend, y = Easy, z = interior
    result = 0.5*x*z + 0.5*y*z
    return result
def tv_conv_f(x, y): # x = Easy, y = tv_conv
    result = x*y
    return result
def people_conv_f(x, y ,z): # x = IE, y = Easy, z = people_conv
    result = 0.5*x*z + 0.5*y*z
    return result
def furniture_f(x, y ,z): # x = IE, y = Age, z = furniture
    x_score = 0.5*x*z
    y_score = 40-y+z
    result = x_score + y_score
    return result

area_score = area_f(SN, JP, area)
interior_score = interior_f(Trend, Easy, interior)
tv_conv_score = tv_conv_f(Easy, tv_conv)
people_conv_score = people_conv_f(IE, Easy, people_conv)
furniture_score = furniture_f(IE, Age, furniture)

total_score = area_score + interior_score + tv_conv_score + people_conv_score + furniture_score
total_score /= 5