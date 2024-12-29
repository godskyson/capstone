import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from datetime import time, datetime
import random


st.header("랜덤 숫자 뽑기")
st.write("숫자를 뽑으세요")

gift = ['배민 상품권', 'CJ 상품권', '스타벅스상품권']
if st.button("숫자 고르기"):
    num = random(gift)
    st.write(num)


# st.header('st.write에 대한 연습')

# st.write('Hello, *World!* **bold** :sunglasses: 이런 것을 쓸 수 있다.')
# st.write(1234)
# st.write('1234')

# # 예제 4
# df = pd.DataFrame({
#     '첫 번째 컬럼' : [1, 2, 3, 4],
#     '두 번째 컬럼' : [10, 20, 30, 40]
#     })

# st.write(df)

# # 예제 5

# df2 = pd.DataFrame(
#     np.random.randn(200, 3),
#     columns=['a', 'b', 'c'])
# c = alt.Chart(df2).mark_circle().encode(
#     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# st.write(c)

# #####################################
# # slider 실습

# st.header('st. slider 실습')
# st.subheader('Slider')

# # 예제 1
# age = st.slider('당신의 나이는?', 0, 130, 25)
# st.write("나는 ", age, '살입니다')

# # 예제 2
# st.subheader('범위 슬라이더')

# values = st.slider(
#     '값의 범위를 선택하세요',
#     0.0, 100.0, (25.0, 75.0))
# st.write('값:', values)

# # 예제 3
# st.subheader('시간 범위 슬라이더')

# appointment = st.slider(
#     "약속을 예약하세요:",
#     value=(time(11, 30), time(12, 45))
# )
# st.write("예약된 시간:", appointment)

# # 예제 4

# st.subheader('날짜 및 시간 슬라이더')

# start_time = st.slider(
#     "언제 시작하시겠습니까?",
#     value=datetime(2024, 1, 1, 9, 30),
#     format="MM/DD/YY - hh:mm"
# )
# st.write("시작 시간:", start_time)


# ###########################
# #st.line_chart 실습

# st.header('라인 차트')

# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c']
# )

# st.line_chart(chart_data)

# ###########################
# #st.selectbox 실습

# st.header('selectbox 실습')

# option = st.selectbox(
#     '가장 좋아하는 색상은 무엇인가요?',
#     ('파랑', '빨강', '초록'),
#     index = None,
#     label_visibility = "visible"
# )

# st.write('당신이 좋아하는 색상은 ', option)

# ###########################
# #st.mutiselect 실습

# st.header('multiselect 실습')

# options = st.multiselect(
#     '가장 좋아하는 색상은 무엇인가요?',
#     ['초록', '노랑', '빨강', '파랑'],
#     ['노랑', '빨강']
# )

# st.write('당신이 선택한 색상:', options)

# ############################
# #st.checkbox 실습

# st.header('st.checkbox')

# st.write('주문하고 싶은 것이 무엇인가요?')

# icecream = st.checkbox('아이스크림')
# coffee = st.checkbox('커피')
# cola = st.checkbox('콜라')

# if icecream:
#     st.write("좋아요! 여기 더 많은 :icecream:")

# if coffee:
#     st.write("알겠씁니다, 여기 커피 있어요. :coffee:")
    
# if cola:
#     st.write("여기 있어요 🥤")
    
