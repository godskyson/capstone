import streamlit as st
import sqlite3
import pandas as pd
import json

USER_DATA_FILE = "user_data.json"

st.set_page_config(page_title="요의정고등학교 위키", layout="wide")

# 사이드바에 로고 이미지 추가
st.sidebar.image("logo.png", use_column_width=True)

# 사이드바에 학교 이름 텍스트 추가
st.sidebar.title("요의정고등학교")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# 사용자 정보 저장 파일


# 사용자 정보 파일 읽기
try:
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

# 회원가입 함수
def signup(username, password):
    if username in users:
        return False, "이미 존재하는 아이디입니다."
    else:
        users[username] = password
        with open(USER_DATA_FILE, "w") as f:
            json.dump(users, f)
        return True, "회원가입에 성공했습니다."

# 로그인 함수
def login(username, password):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True, "로그인에 성공했습니다."
    else:
        return False, "아이디 또는 비밀번호가 잘못되었습니다."

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# 로그인 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# 사용자 정보 저장 파일
USER_DATA_FILE = "user_data.json"

# 사용자 정보 파일 읽기
try:
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}
# 사이드바 메뉴 설정


# 사이드바에 로그인 상태 표시
if st.session_state.logged_in:
    st.sidebar.write(f"{st.session_state.username}님 환영합니다!")
    if st.sidebar.button("로그아웃"):
        logout()
        st.rerun()  # 로그아웃 후 페이지 새로고침
else:
    st.sidebar.write("로그인 페이지로 이동하세요.")
   

# 사이드바 메뉴 설정
#menu = st.sidebar.radio("메뉴", ("메인", "문서", "로그인"))
menu = st.sidebar.radio("메뉴", ("메인", "문서", "로그인", "회원가입"))

if menu == "메인":
    if st.session_state.logged_in:
        st.title("메인 페이지")
        st.write("환영합니다! 다양한 정보를 확인할 수 있습니다.")
    else:
        st.warning("로그인이 필요합니다. 사이드바에서 로그인 페이지로 이동하세요.")

# 문서 페이지
elif menu == "문서":
    if st.session_state.logged_in:
        st.title("문서 페이지")
        st.write("여기는 문서 페이지입니다. 다양한 문서와 자료를 열람할 수 있습니다.")
    else:
        st.warning("로그인이 필요합니다. 사이드바에서 로그인 페이지로 이동하세요.")

# 로그인 페이지
elif menu == "로그인":
    st.title("로그인 페이지")

    if not st.session_state.logged_in:
        username = st.text_input("아이디", key="login_username")
        password = st.text_input("비밀번호", type="password", key="login_password")
        
        if st.button("로그인"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()  # 로그인 후 페이지 새로고침
            else:
                st.error(message)

# 회원가입 페이지
elif menu == "회원가입":
    st.title("회원가입 페이지")

    new_username = st.text_input("아이디", key="signup_username")
    new_password = st.text_input("비밀번호", type="password", key="signup_password")
    confirm_password = st.text_input("비밀번호 확인", type="password", key="signup_confirm_password")

    if st.button("회원가입"):
        if new_password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        elif new_username == "" or new_password == "":
            st.error("아이디와 비밀번호를 모두 입력하세요.")
        else:
            success, message = signup(new_username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

# 메인 페이지
# if menu == "메인":
#     st.title("메인 페이지")
#     st.write("이곳은 메인 페이지입니다. 다양한 정보를 확인할 수 있습니다.")

import streamlit as st
import sqlite3

# SQLite 데이터베이스 설정 및 테이블 초기화
def init_db():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    # 테이블 생성 (없을 경우 생성)
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

# 게시글 작성 함수
def create_post(title, content, author):
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)', (title, content, author))
    conn.commit()
    conn.close()

# 게시글 불러오기 함수
def get_posts():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return posts

# 데이터베이스 초기화
init_db()

# Streamlit 앱 구성
st.title("게시판 웹사이트")

menu = ["게시글 작성", "게시글 열람"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "게시글 작성":
    st.subheader("새 게시글 작성")
    author = st.text_input("작성자 아이디")  # 작성자 아이디 입력란 추가
    title = st.text_input("제목")
    content = st.text_area("내용")
    if st.button("게시글 올리기"):
        if author and title and content:
            create_post(title, content, author)
            st.success("게시글이 성공적으로 등록되었습니다!")
        else:
            st.error("작성자 아이디, 제목, 내용 모두 입력해주세요.")

elif choice == "게시글 열람":
    st.subheader("게시글 목록")
    posts = get_posts()
    if posts:
        for post in posts:
            st.markdown(f"### {post[1]} (작성자: {post[3]})")  # 제목과 작성자 아이디 함께 출력
            st.write(post[2])  # 게시글 내용
            st.markdown("---")
    else:
        st.write("아직 등록된 게시글이 없습니다.")






# 사용자 정보 저장 파일
USER_DATA_FILE = "user_data.json"

# 사용자 정보 파일 읽기
try:
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}



#============================== 문서 데이터베이스

import sqlite3

#+======================익명채팅

import streamlit as st
import time
from datetime import datetime
import random

# 채팅 메시지 저장 리스트
def load_chat_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    return st.session_state["messages"]

def add_chat_message(username, message):
    chat_messages = load_chat_messages()
    chat_messages.append({
        "username": username,
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state["messages"] = chat_messages

# Streamlit 애플리케이션 설정
def main():
    
    # 채팅 위젯
    with st.sidebar.expander("익명 채팅", expanded=True):
        # 사용자 이름 설정
        if "username" not in st.session_state:
            st.session_state["username"] = st.text_input("가상 닉네임을 입력하세요:", value=f"User_{random.randint(1000, 9999)}")

        username = st.session_state["username"]
        st.write(f"당신의 사용자 이름: {username}")

        # 채팅 입력창
        user_message = st.text_input("메시지 입력", "")

        if st.button("전송") and user_message:
            add_chat_message(username, user_message)
            st.rerun()

        # 채팅 메시지 출력
        st.subheader("채팅방")
        chat_messages = load_chat_messages()
        with st.container():
            for chat in chat_messages[-7:]:
                st.write(f"[{chat['time']}] {chat['username']}: {chat['message']}")

if __name__ == "__main__":
    main()
