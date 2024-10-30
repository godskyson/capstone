import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# SQLite 데이터베이스 설정
conn = sqlite3.connect('posts.db', check_same_thread=False)
c = conn.cursor()

# 테이블 생성 (없을 경우 생성)
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, title TEXT, content TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT, timestamp TEXT)''')
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
    c.execute('INSERT INTO posts (username, title, content) VALUES (?, ?, ?)', (username, title, content))
    conn.commit()

# 게시글 불러오기 함수
def get_posts():
    c.execute('SELECT * FROM posts')
    return c.fetchall()

# 게시글 삭제 함수
def delete_post(post_id):
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()

# 채팅 메시지 전송 함수
def send_message(username, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO chat (username, message, timestamp) VALUES (?, ?, ?)', (username, message, timestamp))
    conn.commit()

# 채팅 메시지 불러오기 함수
def get_chat_messages():
    c.execute('SELECT username, message, timestamp FROM chat ORDER BY id ASC')
    return c.fetchall()

# Streamlit 앱 구성
st.title("게시판 및 익명 채팅방 웹사이트")

menu = ["회원가입", "로그인", "게시글 작성", "게시글 열람", "익명 채팅방"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "회원가입":
    st.subheader("회원가입")
    new_username = st.text_input("사용자 이름")
    new_password = st.text_input("비밀번호", type="password")
    if st.button("회원가입 완료"):
        if new_username and new_password:
            if register_user(new_username, new_password):
                st.success("회원가입이 성공적으로 완료되었습니다. 이제 로그인하세요.")
            else:
                st.error("이미 존재하는 사용자 이름입니다. 다른 이름을 선택해주세요.")
        else:
            st.error("사용자 이름과 비밀번호를 모두 입력해주세요.")

elif choice == "로그인":
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

elif choice == "게시글 작성":
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.subheader("새 게시글 작성")
        title = st.text_input("제목")
        content = st.text_area("내용")
        if st.button("게시글 올리기"):
            if title and content:
                create_post(st.session_state.username, title, content)
                st.success("게시글이 성공적으로 등록되었습니다!")
            else:
                st.error("제목과 내용을 모두 입력해주세요.")
    else:
        st.error("로그인이 필요합니다. 먼저 로그인 해주세요.")

elif choice == "게시글 열람":
    st.subheader("게시글 목록")
    posts = get_posts()
    if posts:
        for post in posts:
            st.markdown(f"### {post[2]} (작성자: {post[1]})")
            st.write(post[3])
            if 'logged_in' in st.session_state and post[1] == st.session_state.username:
                if st.button("게시글 삭제", key=f"delete_{post[0]}"):
                    delete_post(post[0])
                    st.success("게시글이 삭제되었습니다.")
            st.markdown("---")
    else:
        st.write("아직 등록된 게시글이 없습니다.")

elif choice == "익명 채팅방":
    st.subheader("익명 채팅방")

    # 채팅 메시지 입력
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        message = st.text_input("메시지 입력")
        if st.button("전송"):
            if message:
                send_message(st.session_state.username, message)
                st.experimental_rerun()
            else:
                st.error("메시지를 입력해주세요.")
    else:
        st.write("채팅에 참여하려면 로그인하세요.")

    # 채팅 메시지 표시
    st.subheader("채팅 기록")
    chat_messages = get_chat_messages()
    for chat in chat_messages:
        st.write(f"[{chat[2]}] {chat[1]}")

# 데이터베이스 연결 종료
conn.close()
