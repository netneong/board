from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def senddata():
    return render_template('index.html', posts = [
    {'id': 1, 'title': '첫 번째 글', 'author': '홍길동'},
    {'id': 2, 'title': '두 번째 글', 'author': '김철수'},
])

if __name__ == '__main__':
    app.run(debug=True) # 코드 저장할 때마다 서버 자동 재시작