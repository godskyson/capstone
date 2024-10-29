import streamlit as st
import sqlite3
import hashlib

# 해시 함수 정의
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# 데이터베이스 연결 및 테이블 생성
def create_usertable():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

def create_post_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS poststable(author TEXT, post TEXT)')
    conn.commit()
    conn.close()

def add_post(author, post):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO poststable(author, post) VALUES (?, ?)', (author, post))
    conn.commit()
    conn.close()

def view_all_posts():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM poststable')
    data = c.fetchall()
    conn.close()
    return data

# Streamlit 애플리케이션 시작
st.title("간단한 웹 애플리케이션")

# 회원가입 및 로그인
menu = ["회원가입", "로그인"]
choice = st.sidebar.selectbox("메뉴", menu)

create_usertable()
create_post_table()

if choice == "회원가입":
    st.subheader("회원가입")
    new_user = st.text_input("사용자 이름")
    new_password = st.text_input("비밀번호", type='password')

    if st.button("회원가입"):
        hashed_new_password = make_hashes(new_password)
        add_userdata(new_user, hashed_new_password)
        st.success("회원가입이 완료되었습니다!")
        st.info("로그인 페이지에서 로그인하세요.")

elif choice == "로그인":
    st.subheader("로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type='password')

    if st.button("로그인"):
        hashed_password = make_hashes(password)
        result = login_user(username, check_hashes(password, hashed_password))
        if result:
            st.success(f"{username}님, 환영합니다!")

            # 게시글 작성 및 열람
            task = st.selectbox("옵션 선택", ["글 작성하기", "글 열람하기"])
            if task == "글 작성하기":
                st.subheader("글 작성하기")
                post_content = st.text_area("게시글 내용")
                if st.button("게시글 업로드"):
                    add_post(username, post_content)
                    st.success("게시글이 업로드되었습니다.")

            elif task == "글 열람하기":
                st.subheader("게시글 열람하기")
                posts = view_all_posts()
                for post in posts:
                    st.write(f"작성자: {post[0]}")
                    st.write(f"내용: {post[1]}")
                    st.write("---")
        else:
            st.warning("사용자 이름 또는 비밀번호가 일치하지 않습니다.")
