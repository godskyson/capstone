import streamlit as st

# 사이드바에 로고 이미지 추가
st.sidebar.image("logo.png", use_column_width=True)

# 사이드바에 학교 이름 텍스트 추가
st.sidebar.title("요의정고등학교")

# 사이드바 메뉴 설정
import streamlit as st

# 사이드바 메뉴 설정
menu = st.sidebar.radio("메뉴", ("메인", "문서", "로그인"))

# 메인 페이지
if menu == "메인":
    st.title("메인 페이지")
    st.write("이곳은 메인 페이지입니다. 다양한 정보를 확인할 수 있습니다.")

# 문서 페이지
# 문서 저장 리스트
def load_documents():
    if "documents" not in st.session_state:
        st.session_state["documents"] = ["기본 문서 내용"]
    return st.session_state["documents"]

def update_document(index, new_content):
    documents = load_documents()
    documents[index] = new_content
    st.session_state["documents"] = documents

# Streamlit 애플리케이션 설정
def main():
    st.title("메인 애플리케이션")

    # 문서 편집 기능
    st.header("문서 편집")
    documents = load_documents()

    for i, doc in enumerate(documents):
        if f"is_editing_{i}" not in st.session_state:
            st.session_state[f"is_editing_{i}"] = False

        if st.session_state[f"is_editing_{i}"]:
            new_content = st.text_area(f"문서 {i + 1} 편집", value=doc, key=f"edit_area_{i}")
            if st.button("저장", key=f"save_button_{i}"):
                update_document(i, new_content)
                st.session_state[f"is_editing_{i}"] = False
                st.rerun()
        else:
            st.write(f"문서 {i + 1}: {doc}")
            if st.button("편집", key=f"edit_button_{i}"):
                st.session_state[f"is_editing_{i}"] = True
                st.rerun()

if __name__ == "__main__":
    main()




import json

# 사용자 정보 저장 파일
USER_DATA_FILE = "user_data.json"

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

# 사이드바 메뉴 설정
menu = st.sidebar.radio("메뉴", ("메인", "문서", "로그인", "회원가입"))

# 사이드바에 로그인 상태 표시
if st.session_state.logged_in:
    st.sidebar.write(f"{st.session_state.username}님 환영합니다!")
    if st.sidebar.button("로그아웃"):
        logout()
        st.rerun()  # 로그아웃 후 페이지 새로고침
else:
    st.sidebar.write("로그인 페이지로 이동하세요.")

# 메인 페이지
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


#wikipedia============================================================

import wikipediaapi

# 위키피디아 검색 함수
def search_wikipedia(query):
    try:
        # 위키피디아 API 객체 생성
        wiki = wikipediaapi.Wikipedia('ko')  # 한국어 위키피디아 사용
        page = wiki.page(query)
        return page if page.exists() else None
    except Exception as e:
        return None

# 페이지 초기화
st.title("위키피디아 검색 클론")
st.write("위키피디아에서 원하는 주제를 검색해보세요!")

# 검색어 입력
query = st.text_input("검색어를 입력하세요:")

if query:
    # 검색 결과 가져오기
    result = search_wikipedia(query)

    # 검색 결과가 있을 경우
    if result:
        st.header(result.title)
        st.write(result.summary[:500] + "...")  # 내용 일부 출력
        st.write(f"[위키피디아에서 더 보기]({result.fullurl})")
    else:
        st.error("해당 검색어에 대한 결과를 찾을 수 없습니다.")


#============================== 문서 데이터베이스

import sqlite3

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect("document_editor.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        content TEXT
    )
''')
conn.commit()

# 함수: 문서 저장
def save_document(title, content):
    try:
        c.execute("INSERT OR IGNORE INTO documents (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        st.success(f"Document '{title}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving document: {e}")

# 함수: 문서 업데이트
def update_document(title, new_content):
    try:
        c.execute("UPDATE documents SET content = ? WHERE title = ?", (new_content, title))
        conn.commit()
        st.success(f"Document '{title}' updated successfully!")
    except Exception as e:
        st.error(f"Error updating document: {e}")

# 함수: 저장된 문서 불러오기
def load_document_titles():
    c.execute("SELECT title FROM documents")
    return [row[0] for row in c.fetchall()]

def load_document_content(title):
    c.execute("SELECT content FROM documents WHERE title = ?", (title,))
    result = c.fetchone()
    return result[0] if result else ""

# Streamlit UI
st.title("Document Editor")

# 메인 페이지에서 문서 선택
st.header("Select or Create a Document")

# 기존 문서 선택 옵션
doc_titles = load_document_titles()
selected_title = st.selectbox("Select an existing document to edit:", [""] + doc_titles)

# 문서 제목 및 내용 입력 필드
if selected_title:
    # 선택된 문서 불러오기
    title = selected_title
    content = load_document_content(selected_title)
    st.subheader(f"Editing Document: {selected_title}")
else:
    title = st.text_input("Enter Document Title")  # 새 문서 제목 입력 필드
    content = ""  # 새 문서 내용 초기화

# 문서 내용 입력 필드 (중앙)
content = st.text_area("Document Content", content, height=300)

# 문서 저장 및 업데이트 버튼
col1, col2 = st.columns(2)  # 두 개의 버튼을 좌우로 나란히 배치

with col1:
    if st.button("Save Document"):
        if title and content:
            save_document(title, content)
        else:
            st.error("Please provide both a title and content.")

with col2:
    if st.button("Update Document"):
        if title and content:
            update_document(title, content)
        else:
            st.error("Please provide both a title and content.")

# 연결 종료
conn.close()


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
    st.title("메인 애플리케이션")

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

