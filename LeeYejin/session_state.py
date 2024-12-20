import streamlit as st

st.title("Session State")

st.subheader("전역변수 Count")

count = 0

if st.button('Increment - 전역변수 Count'):
    count += 1

st.write(f'전역변수 Count: {count}')

st.subheader("st.session_state Count")

# session_state 초기화
if 'count' not in st.session_state:
    st.session_state['count'] = 0

# 초기화
if st.button('Reset'):
    st.session_state['count'] = 0


if st.button('Increment - st.session_state Count'):
    st.session_state['count'] += 1

st.write(f'전역변수 Count: {st.session_state['count']}')

