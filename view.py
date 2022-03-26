# view.py
import urllib.request

import bs4
import pandas as pd
import  tkinter
import tkinter.ttk
from  tkinter import  *
import crowling as c

def show():
    frame = Tk()
    frame.title('서울시 코로나 현황')
    frame.geometry('1100x600+200+100')
    frame.resizable(False,False)

    seoul_new = Button(frame, width=20, height=2, text='서울시 신규 확진자', relief='solid', command=c.seoul_new).place(x=0, y=30)
    seoul_sum = Button(frame, width=20, height=2, text='서울시 누적 확진자', relief='solid', command=c.seoul_sum).place(x=0, y=70)
    area_new = Button(frame, width=20, height=2, text='자치구별 신규 확진자', relief='solid', command=c.area_new).place(x=0, y=110)
    area_sum = Button(frame, width=20, height=2, text='자치구별 누적 확진자', relief='solid', command=c.area_sum).place(x=0, y=150)
    age = Button(frame, width=20, height=2, text='연령대별 확진자', relief='solid', command=c.age).place(x=0, y=190)
    shot = Button(frame, width=20, height=2, text='예방 접종 현황', relief='solid', command=c.shot).place(x=0, y=230)
    sc = Button(frame, width=20, height=2, text='선별진료소', relief='solid', command=c.sc).place(x=0, y=270)
    search = Label(frame, text='url').place(x=350, y=1)
    url_search = Entry(frame, relief='solid', bd=1, width=45)
    url_search.pack()
    url_search.insert(END, "https://www.seoul.go.kr/coronaV/coronaStatus.do")
    val = Entry.get(url_search)

    def sc():
        url_search.delete(0, END)
        web_page = urllib.request.urlopen(val)
        result = bs4.BeautifulSoup(web_page, 'html.parser')
        text.insert(1.0, result)

    button = Button(frame, width=5, text='검색', relief='solid', command=sc).place(x=730, y=0)
    label = Label(frame, text='결과').place(x=200, y=50)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    global  text
    text = Text(frame, relief='solid', bd=1, width=120, height=40, yscrollcommand=scrollbar.set)
    text.pack(side='right')
    scrollbar.config(command=text.yview)
    frame.mainloop()
#================ 결과 텍스트창에 데이터 출력==============
def add_text():
    text.delete(1.0, END)
    new = pd.read_csv('add_new.csv', index_col=0)
    text.insert(1.0, new)
def add_text2():
    text.delete(1.0, END)
    new = pd.read_csv('add_sum.csv', index_col=0)
    text.insert(1.0, new)
def add_text_age():
    text.delete(1.0, END)
    new = pd.read_csv('age.csv', index_col=0)
    text.insert(1.0, new)
def add_text_shot():
    text.delete(1.0, END)
    new = pd.read_csv('shot.csv', index_col=0)
    text.insert(1.0, new)
def add_text_sc():
    text.delete(1.0, END)
    new = pd.read_csv('sc.csv', index_col=0)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    text.insert(1.0, new)
def add_text_area_new():
    text.delete(1.0, END)
    new = pd.read_csv('add_text_area_new.csv', index_col=0)
    text.insert(1.0, new)
def add_text_area_sum():
    text.delete(1.0, END)
    new = pd.read_csv('add_text_area_sum.csv', index_col=0)
    text.insert(1.0, new)
#================ 결과 텍스트창에 데이터 출력 end==============

#==============시각화===============
def seoul_new_see():
    see = Toplevel()
    see.title('시각화')
    see.geometry("100x50")
    btnyes = Button(see, text="그래프로 보기", command=c.seoul_new_graph)
    # btnyes.grid(row=0, column=3)
    btnyes.pack(pady = 10)

def seoul_sum_see():
    see = Toplevel()
    see.title('시각화')
    see.geometry("100x50")
    btnyes = Button(see, text="그래프로 보기", command=c.seoul_sum_graph)
    btnyes.pack(pady = 10)

def age_see():
    see = Toplevel()
    see.title('시각화')
    see.geometry("100x50")
    btnyes = Button(see, text="파이차트로 보기", command=c.seoul_age_pie)
    btnyes.pack(pady = 10)