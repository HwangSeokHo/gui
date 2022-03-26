# covid_19.py

# 크롤링된 결과 저장용 클래스 정의 스크립트

#==================신규 확진자 수==================
class Covid_19_new:
    #멤버변수
    __day = 0
    __new_num = ''

    #생성자
    def __init__(self, day, new_num):
        self.__day = day
        self.__new_num = new_num

    # 연산자 오버로딩 메소드
    # __str__ : 객체 안의 필드 값들을 하나의 문자열로 만들어서 리턴처리함
    def __str__(self):
        return  '서울시 코로나 신규 확진자 수 : {}일 {}'.format(self.__day, self.__new_num)

#==============================================