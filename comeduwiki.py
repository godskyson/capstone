import streamlit as st
import time
from datetime import datetime
import random
import urllib.parse

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
            col1, col2 = st.columns([9, 1])
            with col2:
                if st.button("저장", key=f"save_button_{i}"):
                    update_document(i, new_content)
                    st.session_state[f"is_editing_{i}"] = False
                    st.experimental_rerun()
        else:
            col1, col2 = st.columns([9, 1])
            with col1:
                hyperlink = f'<a href="https://www.youtube.com/watch?v=df9_a4ySCcE" target="_blank">문서 {i + 1}: {doc}</a>'
                st.markdown(hyperlink, unsafe_allow_html=True)
            with col2:
                st.button("편집", key=f"edit_button_{i}", on_click=lambda i=i: enter_edit_mode(i))

    # 사이드바 메뉴 설정
    st.sidebar.title("요의정고등학교")
    st.sidebar.image("logo.png", use_column_width=True)
    menu = st.sidebar.radio("메뉴", ("메인", "문서", "로그인", "회원가입", "챗봇"))

    # 메인 페이지 설정
    if menu == "메인":
        st.title("메인 페이지")
        st.write("이곳은 메인 페이지입니다. 다양한 정보를 확인할 수 있습니다.")
    elif menu == "문서":
        if st.session_state.get("logged_in", False):
            st.title("문서 페이지")
            st.write("여기는 문서 페이지입니다. 다양한 문서와 자료를 열람할 수 있습니다.")
        else:
            st.warning("로그인이 필요합니다. 사이드바에서 로그인 페이지로 이동하세요.")
    elif menu == "로그인":
        st.title("로그인 페이지")
        if not st.session_state.get("logged_in", False):
            username = st.text_input("아이디", key="login_username")
            password = st.text_input("비밀번호", type="password", key="login_password")
            if st.button("로그인"):
                if username == "test" and password == "test":  # 간단한 로그인 예시
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("로그인에 성공했습니다.")
                    st.experimental_rerun()
                else:
                    st.error("아이디 또는 비밀번호가 잘못되었습니다.")
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
                st.success("회원가입에 성공했습니다.")
    elif menu == "챗봇":
        st.title("챗봇")
        st.write("궁금한 점을 물어보세요!")
        user_input = st.text_input("질문: ", key="chat_input")
        if st.button("전송", key="send_button") and user_input:
            # 여기서 OpenAI API 호출을 통해 챗봇 응답을 생성할 수 있습니다.
            # 현재는 임시 응답으로 처리
            chatbot_response = f"챗봇 응답: '{user_input}'에 대한 답변입니다."
            st.write(chatbot_response)

if __name__ == "__main__":
    main()
