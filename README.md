# 메모장으로 활용할 공간

## 1. 가상환경 만들기 `python -m venv [가상환경 이름]
가상환경 사용할때는 venv\Scripts\activate

## 2. 폴더 구조 잡기
templates폴더 생성 이유 Flask를 사용할때 HTML 파일을 찾는 약속된 폴더 이름(이름이 달라지면 Flask가 인식못함)
app.py폴더는 Flask 서버코드가 들어갈 메인 파일

## 3.  Flask 설치 + Hello World 실행
from flask import Flask
app = Flask(__name__) //__name__ = "내 프로젝트 파일들 여기 기준으로 찾아줘" 라고 Flask한테 알려주는 것(templates, static)
// 작동방식__name__의 __file__을 찾음(현재 파일의 주소값을 불러오는 내장변수)
@app.route('/') // @app.route('/')는 URL `/`과 함수 hello_world()를 바인딩시켜서 해당 주소에 접속했을때 함수가 실행되는 기능을 추가하는 데코레이터이다.
def hello_world():
    return 'Hello World!' 

if __name__ == '__main__':
    app.run()

## 4.  CRUD 기능 하나씩 직접 구현
## 5.  SQLite DB 연결
