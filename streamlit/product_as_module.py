import streamlit as st

# session state 초기화 (3개의 값을 관리해봅시다)
# - messages : LLM 질의를 위한 대화내역 >> 계속 대화 쌓아서 연속적 대화 가능케함
# - check_reset > 초기화를 위한 flag

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'system', 'content': 'system_instruction'}
    ]

if 'check_reset' not in st.session_state:
    st.session_state['check_reset'] = False

#------------------------------------------------------#

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from dotenv import load_dotenv
load_dotenv()
import os



def repair_product_information(query):

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
    PINECONE_NAMESPACE=f'{PINECONE_INDEX_NAME}-repair'

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    # 클라이언트 객체
    vector_db = PineconeVectorStore(
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
        namespace=PINECONE_NAMESPACE,
        pinecone_api_key=PINECONE_API_KEY
    )
    # 유사도 검색
    results = vector_db.similarity_search(
        query,
        k=10,
        namespace=PINECONE_NAMESPACE
    )

    return {
        'as_details': query,
        'repair_information': '\n'.join([doc.page_content for doc in results])
    }


def product_repair_cost(query):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """
Persona :
당신은 전자제품에 대한 깊은 사랑과 열정을 가진 서비스센터 직원입니다. 전자 제품에 대한 폭넓은 지식을 보유하고 있으며, 다양한 모델을 제품명만 듣고 어떤 모델 종류인지 구분해내는 능력과 고장난 문제에 따라 필요한 부품 및 수리 비용에 대해 잘 알고 있습니다. 고객이 수리 과정과 비용을 이해할 수 있도록 친근하고 다가가기 쉬운 태도로 설명하며, 초보자도 쉽게 이해할 수 있는 방식으로 설명합니다.

Role:
서비스 센터 직원으로서의 역할은 필요한 수리 부품을 쉽게 이해할 수 있는 방식으로 설명하고 수리 비용 정보를 제공하는 것입니다.  당신은 제품명을 보는 것만으로도 해당 제품이 휴대폰, TV, 노트북, 워치, 탭 중에서 어떤 모델 종류인지 구분할 수 있습니다. 고객이 제품명만 알려줘도 어떤 제품인지 파악하고, 해당하는 수리 부품과 수리 비용을 안내할 수 있어야 합니다. 고객이 최소한의 적합한 수리 부품만 사용하도록 도와 원활한 서비스를 제공합니다. 고객의 불편함을 최소화하고 적절한 부품과 비용을 추천함으로써 고객이 전자 제품을 편리하게 사용할 수 있도록 돕는 것이 목표입니다. 추측성 정보는 고객에게 혼란을 줄 수 있으므로 지양합니다.

Examples:
- 휴대폰 화면 손상 수리에 대한 예시:
고객이 화면 손상으로 인한 수리 비용 설명을 요청하는 경우, 제품의 모델명, 보증 기간, 적합한 수리 부품, 비용, 예상 수리 시간을 초등학생도 이해할 수 있도록 쉽게 설명합니다.

- "왜 TV가 작동하지 않나요?"라는 질문에 대한 예시:
TV가 작동하지 않는 데에는 여러 가지 원인이 있을 수 있습니다. 우선 전원 플러그가 제대로 꽂혀 있는지 확인해주세요. 안테나 케이블 연결이 제대로 되어있지 않거나, 케이블 방송 수신기 또는 위성 리시버의 전원이 꺼져 있을 수 있습니다. 안테나 케이블 연결 상태를 확인하거나, 케이블 방송 수신기 또는 위성 리시버의 전원을 켜주세요. 또한, 환경 조건이 영향을 줄 수 있습니다. 권장 작동 환경은 온도 10℃~40℃(50℉~104℉), 습도 10%~80%이며, 응결이 없는 환경이어야 합니다. 추가적인 문의사항이 있으시면 말씀해주세요. 감사합니다!

        """),
        HumanMessagePromptTemplate.from_template('''
        수리비용 설명에 아래의 제품명과 모델명, 수리부품, 수리비용만을 참고하여 한글로 답변해주세요.
        A/S 내용 :
        {as_details}
        수리 정보 :
        {repair_information}
        ''')
    ])

    model = ChatOpenAI(
        model='gpt-4o',
        temperature=0.3
    )

    output_parser = StrOutputParser()

    chain= prompt | model | output_parser
    return chain.invoke(query)

def answer_gpt(query):
    chain = RunnableLambda(repair_product_information) | RunnableLambda(product_repair_cost)

    # return chain.invoke(query) => answer
    # invoke 실시간이 아니라 stream

    return chain.invoke(query)


