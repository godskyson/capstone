import streamlit as st
import sqlite3
import pandas as pd

# SQLite 데이터베이스 설정
conn = sqlite3.connect('posts.db')
c = conn.cursor()

# 테이블 생성 (없을 경우 생성)
c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
conn.commit()

# 게시글 작성 함수
def create_post(title, content):
    c.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()

# 게시글 불러오기 함수
def get_posts():
    c.execute('SELECT * FROM posts')
    return c.fetchall()

# Streamlit 앱 구성
st.title("게시판 웹사이트")

menu = ["게시글 작성", "게시글 열람"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "게시글 작성":
    st.subheader("새 게시글 작성")
    title = st.text_input("제목")
    content = st.text_area("내용")
    if st.button("게시글 올리기"):
        if title and content:
            create_post(title, content)
            st.success("게시글이 성공적으로 등록되었습니다!")
        else:
            st.error("제목과 내용을 모두 입력해주세요.")

elif choice == "게시글 열람":
    st.subheader("게시글 목록")
    posts = get_posts()
    if posts:
        for post in posts:
            st.markdown(f"### {post[1]}")
            st.write(post[2])
            st.markdown("---")
    else:
        st.write("아직 등록된 게시글이 없습니다.")

# 데이터베이스 연결 종료
conn.close()
