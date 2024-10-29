import streamlit as st
import sqlite3
import pandas as pd

# SQLite 데이터베이스 설정
conn = sqlite3.connect('posts.db')
c = conn.cursor()

# 테이블 생성 (없을 경우 생성)
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, title TEXT, content TEXT)''')
conn.commit()

# 사용자 인증 함수
def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()

# 사용자 등록 함수
def register_user(username, password):
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# 게시글 작성 함수
def create_post(username, title, content):
    try:
        c.execute('INSERT INTO posts (username, title, content) VALUES (?, ?, ?)', (username, title, content))
        conn.commit()
        st.success(f"게시물 '{title}'이(가) 저장되었습니다!")
    except Exception as e:
        st.error(f"게시물 저장 중 오류 발생: {e}")

# 게시글 불러오기 함수
def get_posts():
    c.execute('SELECT * FROM posts')
    return c.fetchall()

# 게시글 삭제 함수
def delete_post(post_id):
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()

# Streamlit 앱 구성
st.title("게시판 웹사이트")

# 로그인 상태
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 로그인 및 로그아웃 기능
if not st.session_state.logged_in:
    st.subheader("회원가입")
    new_username = st.text_input("새 사용자 이름", key="new_username")
    new_password = st.text_input("새 비밀번호", type="password", key="new_password")
    if st.button("회원가입"):
        if new_username and new_password:
            if register_user(new_username, new_password):
                st.success("회원가입이 성공적으로 완료되었습니다. 이제 로그인하세요.")
            else:
                st.error("이미 존재하는 사용자 이름입니다. 다른 이름을 선택해주세요.")
        else:
            st.error("사용자 이름과 비밀번호를 모두 입력해주세요.")

    st.subheader("로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"환영합니다, {username}님!")
        else:
            st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")
else:
    st.sidebar.write(f"로그인된 사용자: {st.session_state.username}")
    if st.sidebar.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("성공적으로 로그아웃되었습니다.")

menu = ["게시글 작성", "게시글 열람"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if st.session_state.logged_in:
    if choice == "게시글 작성":
        st.subheader("새 게시글 작성")
        title = st.text_input("제목")
        content = st.text_area("내용")
        if st.button("게시글 올리기"):
            if title and content:
                create_post(st.session_state.username, title, content)
                st.success("게시글이 성공적으로 등록되었습니다!")
            else:
                st.error("제목과 내용을 모두 입력해주세요.")

    elif choice == "게시글 열람":
        st.subheader("게시글 목록")
        posts = get_posts()
        if posts:
            for post in posts:
                st.markdown(f"### {post[2]} (작성자: {post[1]})")
                st.write(post[3])
                if post[1] == st.session_state.username:
                    if st.button("게시글 삭제", key=f"delete_{post[0]}"):
                        delete_post(post[0])
                        st.success("게시글이 삭제되었습니다.")
                st.markdown("---")
        else:
            st.write("아직 등록된 게시글이 없습니다.")
else:
    st.info("게시글을 작성하거나 열람하려면 로그인이 필요합니다.")

# 데이터베이스 연결 종료
conn.close()
