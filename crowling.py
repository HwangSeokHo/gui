# crowling.py
from html_table_parser import parser_functions
import  urllib.request, bs4
import  oracle_db as oradb
import re
import pandas as pd
import numpy as np
import view as v
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib as mpl

web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do')
result = bs4.BeautifulSoup(web_page, 'html.parser')
find_day = result.find(id= "coronacal")
day_new = find_day.find_all('tr')

mpl.rc('font', family='NanumGothic')    # 한글 설정

#  ==================신규 확진자======================
def seoul_new():
    target = result.find('table', {'class': 't_clndar'})
    tbody = target.find('tbody')
    trData = tbody.find_all('tr')
    tdData = trData[0].find_all('td')
    trDataLen = len(trData)

    list= []
    list2 = []
    for i in range(0, trDataLen):
        tdData = trData[i].find_all(class_='date')
        tdData2 = trData[i].find_all(class_='add_val')
        tdDataLen = len(tdData)
        for j in range(0, tdDataLen):
            element = tdData[j].text
            element2 = tdData2[j].text
            list.append(element)  # 출력하면서 list에 추가
            element2 = re.sub(r"[\t\n\r\(\)\+\,\"]*", "", element2)
            list2.append(element2)
    while '' in list:
        list.remove('')
    while '' in list2:
        list2.remove('')
#================================================
    conn = None
    cursor = None
    query = 'insert INTO COVID_19_SEOUL_NEW VALUES (:1, :2)'
    delete = 'delete from COVID_19_seoul_new'
    try:
        conn = oradb.connect()
        cursor=conn.cursor()
        cursor.execute(delete)
        for i in range(0, len(list2)):  #길이 다르면 디비 저장 안됨 길이가 짧은거 기준
            date = list[i]
            new_num = list2[i]
            new = (date, new_num)
            cursor.execute(query, new)

        oradb.commit(conn)

    except Exception as msg:
         oradb.rollback(conn)
         print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)
    finally:
        cursor.close()
        oradb.close(conn)
#===============================================
    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_seoul_new')
    global  day, num
    day = []
    num = []
    for record in rs:
        day.append(record[0])
        num.append(record[1])
    s = pd.Series(num, index=day)
    s = pd.DataFrame(s, columns=['신규 확진자 수'])  # 시리즈를 데이터프레임으로 변환
    s.to_csv('add_new.csv', mode='w', sep=',')

    v.add_text()    # 결과 텍스트창에 데이터 출력
    v.seoul_new_see()     # 말풍선?
#  ==================신규 확진자 end=====================
# ==============신규 확진자 시각화=================

def seoul_new_graph():
    y = num
    b = list(map(int, y))   # 기록된 값 str -> int 형변환  / 숫자 사이에 , 있으면 안됨
    bb = b[-7:]     # 최근 7일만 보여지게
    x= day
    xx = x[-7:]

    plt.bar(xx, bb)
    plt.xticks(xx)
    plt.xlabel("날짜")
    plt.ylabel("확진자 수")
    # for i, v in enumerate(xx):
    #     plt.text(v, y[i], y[i], fontsize = 9, horizontalalignment='center')
    plt.show()

# ==============신규 확진자 시각화 end=================


#  ==================누적 확진자======================
def seoul_sum():
    target = result.find('table', {'class': 't_clndar'})
    tbody = target.find('tbody')
    trData = tbody.find_all('tr')
    tdData = trData[0].find_all('td')
    trDataLen = len(trData)

    list = []
    list2 = []
    for i in range(0, trDataLen):
        tdData = trData[i].find_all(class_='date')
        tdData2 = trData[i].find_all(class_='tot_val')
        tdDataLen = len(tdData)
        for j in range(0, tdDataLen):
            element = tdData[j].text
            element2 = tdData2[j].text
            list.append(element)  # 출력하면서 list에 추가
            element2 = re.sub(r"[\t\n\r\(\)\+\,\"]*", "", element2)
            list2.append(element2)
    while '' in list:
        list.remove('')
    while '' in list2:
        list2.remove('')

    conn = None
    cursor = None
    query = 'insert INTO COVID_19_seoul_sum VALUES (:1, :2)'
    delete = 'delete from COVID_19_seoul_sum'
    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)
        for i in range(0, len(list2)):  # 길이 다르면 디비 저장 안됨 길이가 짧은거 기준
            date = list[i]
            new_num = list2[i]
            new = (date, new_num)
            cursor.execute(query, new)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)
    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_seoul_sum')
    global day1, num1
    day1 = []
    num1 = []
    for record in rs:
        day1.append(record[0])
        num1.append(record[1])
    s = pd.Series(num1, index=day1)
    s = pd.DataFrame(s, columns=['누적 확진자 수'])  # 시리즈를 데이터프레임으로 변환
    s.to_csv('add_sum.csv', mode='w', sep=',')

    v.add_text2()
    v.seoul_sum_see()
#  ==================누적 확진자 end======================
# ==============누적 확진자 시각화=================
def seoul_sum_graph():
    y = num1
    b = list(map(int, y))  # 기록된 값 str -> int 형변환  / 숫자 사이에 , 있으면 안됨
    bb = b[-7:]
    x = day1
    xx = x[-7:]
    plt.bar(xx, bb)
    plt.xticks(xx)
    plt.show()

# ==============누적 확진자 시각화 end=================

# ================== 지역 신규 =====================
def area_new():
    web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do')
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    target = result.find('table', {'class': 'tstyle-status pc pc-table'})

    data = parser_functions.make2d(target)
    df = pd.DataFrame(data)

    a = data[0]
    b = data[1]
    c = data[2]
    d = data[3]
    e = data[4]
    f = data[5]

    conn = ''
    cursor = ''
    query = 'insert into covid_19_area_new values (:1, :2)'
    delete = 'delete from covid_19_area_new'
    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)
        result_list = None
        for i in range(0, len(a)):
            area = a[i]
            new_coronic = c[i]

            result_list = (area, new_coronic)
            cursor.execute(query, result_list)

        result_list = None
        for l in range(0, len(d)):
            area = d[l]
            new_coronic = f[l]

            result_list = (area, new_coronic)
            cursor.execute(query, result_list)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)

    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_area_new')
    global  date, num2
    date = []
    num2 = []
    for record in rs:
        date.append(record[0])
        num2.append(record[1])
    s = pd.Series(num2, index=date)
    s = pd.DataFrame(s, columns=['신규 확진자 수'])
    s.to_csv('add_text_area_new.csv', mode='w', sep=',')
    v. add_text_area_new()

# ================== 지역 신규 end=====================


# ================== 지역 누적 =====================
def area_sum():
    web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do')
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    target = result.find('table', {'class': 'tstyle-status pc pc-table'})

    data = parser_functions.make2d(target)
    df = pd.DataFrame(data)

    a = data[0]
    b = data[1]
    c = data[2]
    d = data[3]
    e = data[4]
    f = data[5]

    conn = ''
    cursor = ''
    query = 'insert into covid_19_area_sum values (:1, :2)'
    delete = 'delete from covid_19_area_sum'
    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)
        result_list = None
        for j in range(0, len(a)):
            area = a[j]
            sum_coronic = b[j]

            result_list = (area, sum_coronic)
            cursor.execute(query, result_list)

        result_list = None
        for k in range(0, len(d)):
            area = d[k]
            sum_coronic = e[k]

            result_list = (area, sum_coronic)
            cursor.execute(query, result_list)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)

    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_area_sum')

    date = []
    num = []
    for record in rs:
        date.append(record[0])
        num.append(record[1])
    s = pd.Series(num, index=date)
    s = pd.DataFrame(s, columns=['누적 확진자 수'])
    s.to_csv('add_text_area_sum.csv', mode='w', sep=',')
    v.add_text_area_sum()
# ================== 지역 누적 end=====================


# ================== 연령대 =====================
def age():
    web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do')
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    target = result.find('table', {'class': 'tstyle-status tstyle-corona'})

    data = parser_functions.make2d(target)
    df = pd.DataFrame(data=data[1:], columns=data[0])
    global age1, ratio1
    age1 = data[0]
    confirmed_case1 = data[1]
    ratio1 = data[2]

    conn = ''
    cursor = ''
    query = 'insert into COVID_19_AGE values (:1, :2, :3)'
    delete = 'delete from COVID_19_AGE'
    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)

        covid_age = None
        for i in range(0, len(age1)):
            age = age1[i]
            confirmed_case = confirmed_case1[i]
            ratio = ratio1[i]

            covid_age = (age, confirmed_case, ratio)
            cursor.execute(query, covid_age)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)
    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_AGE')

    d = pd.DataFrame(age1)
    e = pd.DataFrame(confirmed_case1)
    f = pd.DataFrame(ratio1)
    s = pd.concat([d,e,f], axis=1)
    
    s.to_csv('age.csv', mode='w', sep=',')
    v.add_text_age()
    v.age_see()
# age()
# ================== 연령대 end=====================

#================= 얀령대 시각화================
def seoul_age_pie():

    age_list=[]
    ratio_list=[]
    for i in age1[2:]:          #리스트에서 필요한 값만 추출 3번째 부터
        age_list.append(i)
    for i in ratio1[2:]:
        ratio_list.append(i)

    sizes = ratio_list
    plt.title("Pie Chart")
    plt.pie(sizes, labels=age_list, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.show()
# ================= 얀령대 시각화 end================

# ================== 예방접종 =====================
def shot():
    web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=47')
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    target = result.find('table', {'class': 'status-organ-new-type4 type1'})

    data = parser_functions.make2d(target)
    df = pd.DataFrame(data)

    dday1 = data[0]
    st_inoculation1 = data[1]
    nd_inoculation1 = data[2]
    booster_vaccination1 = data[3]

    conn = ''
    cursor = ''
    query = 'insert into COVID_19_SHOT values (:1, :2, :3, :4)'
    delete = 'delete from COVID_19_SHOT'

    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)

        covid_shot = None
        for i in range(0, len(dday1)):
            dday = dday1[i]
            st_inoculation = st_inoculation1[i]
            nd_inoculation = nd_inoculation1[i]
            booster_vaccination = booster_vaccination1[i]

            covid_shot = (dday, st_inoculation, nd_inoculation, booster_vaccination)
            cursor.execute(query, covid_shot)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)
    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_SHOT')

    d = pd.DataFrame(dday1)
    e = pd.DataFrame(st_inoculation1)
    f = pd.DataFrame(nd_inoculation1)
    t = pd.DataFrame(booster_vaccination1)
    s = pd.concat([d, e, f, t], axis=1)
    s.to_csv('shot.csv', mode='w', sep=',')
    v.add_text_shot()
# ================== 예방접종 end=====================
# ================== 선별진료소 =====================
def sc():
    web_page = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=03')
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    target = result.find('table', {'class': 'tb_base tb_imsi'})

    data = parser_functions.make2d(target)
    df = pd.DataFrame(data[1:])

    area1 = df[1]
    division1 = df[2]
    place1 = df[3]
    place_term1 = df[4]
    operating1 = df[5]
    disinfection_time1 = df[6]

    conn = ''
    cursor = ''
    query = 'insert into COVID_19_SC values (:1, :2, :3, :4, :5, :6)'
    delete = 'delete from COVID_19_SC'
    try:
        conn = oradb.connect()
        cursor = conn.cursor()
        cursor.execute(delete)

        covid_sc = None
        for i in range(0, len(area1)):
            area = area1[i]
            division = division1[i]
            place = place1[i]
            place_term = place_term1[i]
            operating = operating1[i]
            disinfection_time = disinfection_time1[i]

            covid_sc = (area, division, place, place_term, operating, disinfection_time)
            cursor.execute(query, covid_sc)

        oradb.commit(conn)

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터베이스 과제용계정  테이블 기록 관련 에러', msg)
    finally:
        cursor.close()
        oradb.close(conn)

    conn = oradb.connect()
    cursor = conn.cursor()
    rs = cursor.execute('SELECT * FROM COVID_19_SC')

    s = pd.DataFrame(area1)
    b = pd.DataFrame(division1)
    c = pd.DataFrame(place1)
    d = pd.DataFrame(place_term1)
    e = pd.DataFrame(operating1)
    f = pd.DataFrame(disinfection_time1)
    df_row = pd.concat([s, b, c, d, e, f], axis=1)
    df_row.to_csv('sc.csv', mode='w', sep=',')
    v.add_text_sc()
# ================== 선별진료소 end=====================
