import streamlit as st

st.set_page_config(page_title="요의정고등학교 위키", layout="wide")
st.title("익명 채팅방")


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

def main():
    st.title("사용자 문서 관리 페이지")
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if st.session_state.edit_mode:
        edit_document()
    else:
        show_document()

def show_document():
    st.header("사용자 정보")
    
    # 기본 사용자 정보 표시
    name = st.session_state.get('name', '홍길동')
    age = st.session_state.get('age', 30)
    education = st.session_state.get('education', '대학교 졸업')
    hobby = st.session_state.get('hobby', '등산')
    
    st.write(f"**이름:** {name}")
    st.write(f"**나이:** {age}")
    st.write(f"**학력:** {education}")
    st.write(f"**취미:** {hobby}")
    
    if st.button("문서 편집하기"):
        st.session_state.edit_mode = True




# 문서 페이지
# 문서 저장 리스트
# def load_documents():
#     if "documents" not in st.session_state:
#         st.session_state["documents"] = ["기본 문서 내용"]
#     return st.session_state["documents"]

# def update_document(index, new_content):
#     documents = load_documents()
#     documents[index] = new_content
#     st.session_state["documents"] = documents

# Streamlit 애플리케이션 설정
# def main():
#     st.title("메인 애플리케이션")

#     # 문서 편집 기능
#     st.header("문서 편집")
#     documents = load_documents()

#     for i, doc in enumerate(documents):
#         if f"is_editing_{i}" not in st.session_state:
#             st.session_state[f"is_editing_{i}"] = False

#         if st.session_state[f"is_editing_{i}"]:
#             new_content = st.text_area(f"문서 {i + 1} 편집", value=doc, key=f"edit_area_{i}")
#             if st.button("저장", key=f"save_button_{i}"):
#                 update_document(i, new_content)
#                 st.session_state[f"is_editing_{i}"] = False
#                 st.rerun()
#         else:
#             st.write(f"문서 {i + 1}: {doc}")
#             if st.button("편집", key=f"edit_button_{i}"):
#                 st.session_state[f"is_editing_{i}"] = True
#                 st.rerun()

# if __name__ == "__main__":
#     main()




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


def create_database():
    # SQLite 데이터베이스 연결 및 테이블 생성
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    education TEXT,
                    hobby TEXT
                )''')
    conn.commit()
    conn.close()

def get_all_users():
    # 모든 사용자 데이터 가져오기
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM user_data")
    users = c.fetchall()
    conn.close()
    return users

def add_user_to_db(name, age, education, hobby):
    # 사용자 데이터 추가
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO user_data (name, age, education, hobby) VALUES (?, ?, ?, ?)", (name, age, education, hobby))
    conn.commit()
    conn.close()

def update_user_in_db(user_id, name, age, education, hobby):
    # 사용자 데이터 업데이트
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("UPDATE user_data SET name = ?, age = ?, education = ?, hobby = ? WHERE id = ?", (name, age, education, hobby, user_id))
    conn.commit()
    conn.close()

def main():
    create_database()

    st.title("사용자 문서 열람 및 편집")
    
    # 모든 사용자 데이터 가져오기
    users = get_all_users()
    st.subheader("사용자 목록")
    for user in users:
        st.write(f"ID: {user[0]}, 이름: {user[1]}, 나이: {user[2]}, 학력: {user[3]}, 취미: {user[4]}")
    
    # 문서 편집 버튼
    if st.button("새 사용자 추가하기"):
        add_new_user()
    
    # 사용자 선택 및 편집
    user_id = st.number_input("편집할 사용자 ID 입력", min_value=1, step=1)
    if st.button("문서 편집하기"):
        edit_document(user_id)

def add_new_user():
    st.subheader("새 사용자 추가하기")
    
    # 사용자 정보 입력 폼
    with st.form("add_form"):
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=0, step=1)
        education = st.text_input("학력")
        hobby = st.text_input("취미")
        
        # 제출 버튼
        submitted = st.form_submit_button("저장하기")
        
        if submitted:
            # 데이터베이스에 사용자 추가
            add_user_to_db(name, age, education, hobby)
            st.success("새 사용자가 성공적으로 추가되었습니다.")

def edit_document(user_id):
    users = get_all_users()
    user_data = None
    for user in users:
        if user[0] == user_id:
            user_data = user
            break

    if user_data:
        st.subheader("문서 편집하기")
        
        # 사용자 정보 수정 폼
        with st.form("edit_form"):
            new_name = st.text_input("이름", user_data[1])
            new_age = st.number_input("나이", value=user_data[2], min_value=0, step=1)
            new_education = st.text_input("학력", user_data[3])
            new_hobby = st.text_input("취미", user_data[4])
            
            # 제출 버튼
            submitted = st.form_submit_button("저장하기")
            
            if submitted:
                # 수정된 정보 업데이트
                update_user_in_db(user_id, new_name, new_age, new_education, new_hobby)
                st.success("사용자 정보가 성공적으로 업데이트되었습니다.")
    else:
        st.error("해당 ID의 사용자를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()


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

import firebase_admin
from firebase_admin import credentials, db
import time

# Firebase 설정 초기화
cred = credentials.Certificate("path/to/your-firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com'
})

# 채팅 메세지를 저장할 경로 설정
chat_ref = db.reference('chat')

# Streamlit 사용자 인터페이스 정의
def main():
    st.title("실시간 채팅")

    username = st.text_input("사용자 이름", "")
    message = st.text_input("메시지를 입력하세요", "")

    if st.button("보내기"):
        if username and message:
            chat_ref.push({
                'username': username,
                'message': message,
                'timestamp': time.time()
            })

    st.write("### 채팅 기록")

    messages = chat_ref.order_by_child('timestamp').get()
    if messages:
        for key, value in messages.items():
            st.write(f"{value['username']}: {value['message']}")

if __name__ == "__main__":
    main()



