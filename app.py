from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

posts = [
    {'id': 1, 'title': '첫 번째 글', 'author': '홍길동', 'content': '첫 번째 글의 내용입니다.', 'date': '2026-03-22 11:34'},
    {'id': 2, 'title': '두 번째 글', 'author': '김철수', 'content': '두 번째 글의 내용입니다.', 'date': '2026-03-22 22:12'},
]
next_id = 3

# 바인딩: 식별자와 객체를 연결하는 것을 말한다.
@app.route('/') # 데코레이터의 url'/'과 함수 hello_world()를 바인딩시켜서 사이트에 접속하면 함수 사용
def dashboard():
    return render_template('index.html', posts=posts) # 두번째 인자/ 변수명:[html파일(템플릿) 안에서 이 데이터를 부를 이름] / 파이썬 코드(서버)에서 미리 만든 실제 데이터


"""흐름도로 보는 if-else(글쓰기 화면보기, 저장을 한번에 처리할 수 있도록 한다.)
1. 사용자: /write 접속 (GET 요청)

2. Flask: if 통과 - else 실행 - write.html 전송 (화면 등장)

3. 사용자: 내용 작성 후 '저장' 클릭 (POST 요청)

4. Flask: if문 적중! - 데이터 DB 저장 - redirect로 다른 곳으로 보냄"""
@app.route('/write', methods=['GET', 'POST']) # /write url과 write()함수를 바인딩시켜서 사이트의 /write에 접속되면 GET과 POST 요청을 허락
def write():
    global next_id
    
    if request.method == 'POST': # 데이터를 실제로 저장
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        post = {
            'id': next_id,
            'title': title,
            'author': author,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M') 
        }
        posts.append(post)
        next_id += 1
        return redirect(url_for('dashboard')) # url_for()는 함수 이름을 문자열로 받아 바인딩되어있는 URL을 반환한다., redirect()는 브라우저에 이동명령을 전달한다.
    else:
        return render_template('write.html') # 글쓰기 화면을 보여주는 get요청
    
@app.route('/post/<int:post_id>') # URL에 변수를 넣는 방법
def detail(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    # 글이 없으면 404 에러 반환
    if post is None:
        return "글을 찾을 수 없습니다.", 404
    
    # 찾은 글을 detail.html로 넘기기
    return render_template('detail.html', post=post)

@app.route('/edit/<int:post_id>', methods =['GET', 'POST'])
def edit(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if post is None:
        return "글을 찾을 수 없습니다.", 404
    
    if request.method == 'POST': # 데이터를 실제로 저장
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        post['title'] = title
        post['author'] = author
        post['content'] = content
       
        return redirect(url_for('detail', post_id=post_id)) # url_for()는 함수 이름을 문자열로 받아 바인딩되어있는 URL을 반환한다., redirect()는 브라우저에 이동명령을 전달한다.
    else:
        return render_template('edit.html', post=post) # 수정 화면을 보여주는 get요청

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global posts
    
    # 리스트 컴프리헨션: post_id가 일치하지 않는 항목들만 남겨서 posts를 갱신합니다.
    posts = [post for post in posts if post['id'] != post_id]
    
    # 삭제 후 메인 페이지(또는 목록 페이지)로 돌아갑니다.
    return redirect(url_for('dashboard'))        

if __name__ == '__main__':
    app.run(debug=True) # 코드 저장할 때마다 서버 자동 재시작