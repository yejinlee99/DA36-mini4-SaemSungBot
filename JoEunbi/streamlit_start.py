import streamlit as st
from PIL import Image
import time

# 세션 상태 초기화
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.page = 'intro'

# 전체 페이지 설정
st.set_page_config(
    page_title="SAEMSUNGBOT",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS 스타일링
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f7f7;
    }
    .custom-title {
        text-align: center;
        font-size: 4em;
        font-weight: bold;
        color: #494a4e;
        letter-spacing: 0.1em;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .centered-text {
        font-size: 1.5em;
        font-weight: bold;
        color: #494a4e;
        text-align: left;
        padding-left: 20px;
        display: flex;
        align-items: center;
        height: 100%;
    }
    .stButton > button {
        background-color: #494a4e;
        color: white;
        border-radius: 5px;
        border: 2px solid #494a4e;
        padding: 0.5em 1em;
        min-width: 150px;
    }
    .stButton > button:hover {
        background-color: #44dab1;
        border: 2px solid #44dab1;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # intro_page
    if st.session_state.page == 'intro':
        with st.empty():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                intro_image = Image.open('./intro.png')
                st.image(intro_image, use_container_width=True)
        time.sleep(3)
        st.session_state.page = 'home'
        st.rerun()

    # home_page
    elif st.session_state.page == 'home':
        st.markdown('<div class="custom-title">SAEMSUNGBOT</div>', unsafe_allow_html=True)

        col_main1, col_main2, col_main3 = st.columns([1, 2, 1])
        with col_main2:
            col_img, col_text = st.columns([1, 1.5])
            with col_img:
                saemsungbot_image = Image.open('./samsung.jpg')
                st.image(saemsungbot_image.resize((200, 200)), use_container_width=True)
            with col_text:
                st.markdown('<div class="centered-text">어떤 도움이 필요하신가요?<br>성심성의껏 답변드릴게요.</div>',
                            unsafe_allow_html=True)

        col_buttons = st.columns([1, 1, 1, 0.2, 1, 1, 1])
        with col_buttons[2]:
            if st.button('제품 문의', use_container_width=True):
                st.session_state.page == 'product_manual'
                st.write("제품 사용방법에 대한 문의 페이지로 이동합니다.")
        with col_buttons[4]:
            if st.button('수리비 문의', use_container_width=True):
                st.write("예상 수리비 확인 페이지로 이동합니다.")

if __name__ == "__main__":
    main()