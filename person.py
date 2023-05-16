



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
