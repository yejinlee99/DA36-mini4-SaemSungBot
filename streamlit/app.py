from PIL import Image
import time
import streamlit as st
from streamlit_chat import message as msg
import product_manual_module as pmm
import product_as_module as pam

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
    .page-title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #494a4e;
        margin-bottom: 10px;
    }
    .page-subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #494a4e;
        margin-bottom: 30px;
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

def change_page(new_page):
    st.session_state.page = new_page
    st.rerun()


def main():
    # intro_page
    if st.session_state.page == 'intro':
        with st.empty():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                intro_image = Image.open('./intro.png')
                st.image(intro_image, use_container_width=True)
        time.sleep(3)
        change_page('home')

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
            if st.button('제품 문의', icon='💻', use_container_width=True):
                change_page('saemsungbot_manual')
        with col_buttons[4]:
            if st.button('수리비 문의', icon='👩‍🔧', use_container_width=True):
                change_page('saemsungbot_repair')

#-heo-----------------------------------------------------------------------------------------------------------------------------#
    # manual_page
    elif st.session_state.page == 'saemsungbot_manual':
        st.markdown('<div class="page-title">제품에 관련한 문의</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">편하게 문의해주세요! 샘숭봇이 알려드리겠습니다.🤖</div>', unsafe_allow_html=True)

        # 필요한 기본 변수 선언

        if 'option' not in st.session_state:
            st.session_state["option"] = 'select'

        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {'role': 'system', 'content': '당신은 친절한 삼성 전자 챗봇입니다'}
            ]

        if 'check_reset' not in st.session_state:
            st.session_state['check_reset'] = False

        product = pmm.product
        product_list = list(product.keys())
        product_list.insert(0, 'select')

        def write_query():
            st.write(f" 👩🏻‍💻{st.session_state["option"]} 제품에 대해 궁금한 점을 적어주세요 ! ")
            query = st.chat_input("")
            if query is not None:
                st.session_state["messages"].append({'role': 'user', "content": query})
                response = pmm.ai_product_manual({'query': st.session_state["messages"],
                                                  'product': st.session_state["option"]})
                st.session_state["messages"].append({'role': 'assistant', "content": response})  # gpt의 role은 assistant
                st.subheader("질문/답변")
                return response

        # 메인 컨텐츠 영역
        col_manual1, col_manual2, col_manual3 = st.columns([1, 2, 1])
        with col_manual2:
            st.session_state["option"] = st.selectbox('model selection', product_list, index=0)
            if st.session_state["option"] != 'select' and st.session_state['check_reset'] is False:
                answer = write_query()


                for i, message in enumerate(st.session_state["messages"]):
                    role = message["role"]
                    content = message["content"]
                    if role == "user":
                        msg(content, is_user=True, key=str(i))  # streamlit chat module에 있는 method
                    elif role == "assistant" and answer is not None:
                        st.write_stream(content)


            else:
                st.session_state['option'] = 'select'
                st.session_state["check_reset"] = False
                st.session_state['messages'] = [
                    {'role': 'system', 'content': '당신은 친절한 챗봇입니다'}
                ]



        # 하단 버튼 영역
        st.write("")
        st.write("")
        col_manual_buttons = st.columns([1.5, 1, 1, 1.5])
        with col_manual_buttons[1]:
            if st.button('홈으로 돌아가기', icon='🏠', use_container_width=True):
                change_page('home')
        with col_manual_buttons[2]:
            if st.button('다른 제품 문의하기', icon='🔍', use_container_width=True):
                st.session_state['messages'] = [
                    {'role': 'system', 'content': "system_instruction"}
                ]
                st.session_state['option'] = 'select'
                st.session_state['check_reset'] = True  # 화면 초기화를 위한 !!

                st.rerun()
# -heo-----------------------------------------------------------------------------------------------------------------------------#


# -lee---------------------------------------------------------------------------------------------------------------------------------#
    # repair_page

    elif st.session_state.page == 'saemsungbot_repair':
        st.markdown('<div class="page-title">수리비 문의</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">편하게 문의해주세요! 샘숭봇이 알려드리겠습니다.🤖</div>', unsafe_allow_html=True)

        # 대화 기록 초기화 (한 번만 수행)
        if "repair_messages" not in st.session_state:
            st.session_state.repair_messages = []

        # 메인 컨텐츠 영역
        col_repair1, col_repair2, col_repair3 = st.columns([1, 2, 1])

        with col_repair2:
            st.subheader("질문/답변")
            st.write("제품에 대해 궁금한 점을 적어주세요 ! ")
            user_input = st.text_input("메세지를 적어주세요.")

            if user_input:
                # 사용자의 질문 추가
                st.session_state.repair_messages.append(user_input)
                with st.chat_message("user"):
                    st.markdown(user_input)

                # GPT 응답 생성
                query = pam.answer_gpt(user_input)
                st.session_state.repair_messages.append(query)

                with st.chat_message("assistant"):
                    st.markdown(query)

        # 하단 버튼 영역
        st.write("")
        st.write("")
        col_manual_buttons = st.columns([1, 2, 1])
        with col_manual_buttons[1]:
            if st.button('홈으로 돌아가기', icon='🏠', use_container_width=True):
                change_page('home')


if __name__ == "__main__":
    main()