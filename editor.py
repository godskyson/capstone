import streamlit as st
import sqlite3

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
