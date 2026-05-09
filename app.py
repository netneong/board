import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

posts = [
    {'id': 1, 'title': '첫 번째 글', 'author': '홍길동',
        'content': '첫 번째 글의 내용입니다.', 'date': '2026-03-22 11:34'},
    {'id': 2, 'title': '두 번째 글', 'author': '김철수',
        'content': '두 번째 글의 내용입니다.', 'date': '2026-03-22 22:12'},
]
next_id = 3


def init_db():
    conn = sqlite3.connect('board.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        title   TEXT    NOT NULL,
        author  TEXT    NOT NULL,
        content TEXT    NOT NULL,
        date    TEXT    NOT NULL
    )
''')

    # 기본 데이터 삽입 — 테이블이 비어있을 때만 넣기
    cursor.execute('SELECT COUNT(*) FROM posts')
    count = cursor.fetchone()[0]

    if count == 0:  # 데이터가 없을 때만 삽입
        cursor.execute('''
            INSERT INTO posts (title, author, content, date)
            VALUES (?, ?, ?, ?)
        ''', ('첫 번째 글', '홍길동', '첫 번째 글의 내용입니다.', '2026-03-22 11:34'))

        cursor.execute('''
            INSERT INTO posts (title, author, content, date)
            VALUES (?, ?, ?, ?)
        ''', ('두 번째 글', '김철수', '두 번째 글의 내용입니다.', '2026-03-22 22:12'))

    conn.commit()
    conn.close()

# 바인딩: 식별자와 객체를 연결하는 것을 말한다.


@app.route('/')  # 데코레이터의 url'/'과 함수 hello_world()를 바인딩시켜서 사이트에 접속하면 함수 사용
def dashboard():
    conn = sqlite3.connect('board.db')
    conn.row_factory = sqlite3.Row  # 기본으로 받는 형태가 튜플이여서 딕셔너리로 바꾸기
    cursor = conn.cursor()

    # 1. SQL로 전체 글 가져오기
    cursor.execute('SELECT * FROM posts')

    # 2. 결과를 모두 가져오기
    rows = cursor.fetchall()

    conn.close()

    # 3. rows를 index.html로 넘기기
    # 두번째 인자/ 변수명:[html파일(템플릿) 안에서 이 데이터를 부를 이름] / 파이썬 코드(서버)에서 미리 만든 실제 데이터
    return render_template('index.html', posts=rows)


"""흐름도로 보는 if-else(글쓰기 화면보기, 저장을 한번에 처리할 수 있도록 한다.)
1. 사용자: /write 접속 (GET 요청)

2. Flask: if 통과 - else 실행 - write.html 전송 (화면 등장)

3. 사용자: 내용 작성 후 '저장' 클릭 (POST 요청)

4. Flask: if문 적중! - 데이터 DB 저장 - redirect로 다른 곳으로 보냄"""


# /write url과 write()함수를 바인딩시켜서 사이트의 /write에 접속되면 GET과 POST 요청을 허락
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST': # 데이터를 실제로 저장
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        date = datetime.now().strftime('%Y-%m-%d %H:%M')

        conn = sqlite3.connect('board.db')
        cursor = conn.cursor()

        # DB에 INSERT
        cursor.execute('''
         INSERT INTO posts (title, author, content, date)
         VALUES (?, ?, ?, ?)
        ''', (title, author, content, date))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    else:
        return render_template('write.html') 

@app.route('/post/<int:post_id>')  # URL에 변수를 넣는 방법
@app.route('/post/<int:post_id>')
def detail(post_id):
    conn = sqlite3.connect('board.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # id가 일치하는 글 하나만 가져오기
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()  # fetchall 대신 fetchone 사용
    
    conn.close()
    
    if post is None:
        return "글을 찾을 수 없습니다.", 404
    
    return render_template('detail.html', post=post)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = sqlite3.connect('board.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        # UPDATE SQL 작성
        cursor.execute('''
            UPDATE posts SET title=?, content=?
            WHERE id=?
        ''', (title, content, post_id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('detail', post_id=post_id))
    else:
        cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        post = cursor.fetchone()
        conn.close()
        return render_template('edit.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = sqlite3.connect('board.db')
    cursor = conn.cursor()
    
    # DELETE SQL 작성
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # 코드 저장할 때마다 서버 자동 재시작
