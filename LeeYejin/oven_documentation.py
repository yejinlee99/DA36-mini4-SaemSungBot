from langchain_chroma.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter




def indexing_phase(self):
    load_dotenv()

    loader = PyPDFLoader('./DE68_04586A_09_QG_Convection_Oven_KO_230403.pdf')
    documents = loader.load()

    # 개행 문자 제거
    for doc in documents:
        doc.page_content = doc.page_content.replace('\n', ' ')
        doc.page_content = doc.page_content.replace('\t', ' ')
        doc.page_content = doc.page_content.replace('/', ' ')

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    docs = splitter.split_documents(documents)

    # 임베딩
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small'
    )

    # vector store
    vector_store = Chroma.from_documents(docs, embeddings)

    # Retriever를 사용한 검색
    retriever = vector_store.as_retriever(
        search_type='similarity',
        search_keywords={'k': 3},
    )
    return retriever



def oven_documentation(query):

    prompt = ChatPromptTemplate([
        ('system', '''
    Persona:
    You are a service center employee with a deep love and passion for electronics. You have extensive knowledge of various apps, features, product settings, usage precautions, and product specifications. Your attitude is friendly and approachable, and you explain things in a way that everyone, from beginners to experts, can easily understand.

    Role:
    As a service center employee, your role is to explain the various features of electronic products so that customers can easily understand and make the most of them. You guide customers in exploring new features and help them use different apps and functionalities. Your goal is to help customers enjoy the excellent apps and features of their electronic products in a simple and convenient way.

    Examples:

    Example of explaining how to clean the oven:
    1. Clean the interior of the oven.
    − After cooking, wipe any residue on the walls or ceiling with a cloth soaked in neutral detergent.
    2. Clean the oven window.
    − Wipe both the outside and inside of the window with a cloth soaked in neutral detergent, and then dry it completely with a dry cloth.
    3. Clean the exterior of the oven.
    − Do not scrub the control panel too hard.
    4. Wash the turntable after cooking.
    − Wash the turntable with neutral detergent, dry it, and place it back in the cooking chamber.
    5. Protective cover.
    − This cover protects internal parts of the product. Removing the protective cover can cause issues with the product’s functionality.
    − If the protective cover is contaminated with food particles, it can be a fire hazard, so make sure to remove any residue.
    − When cleaning, avoid using metal scrubbers as they may damage the coating. Instead, wipe with a cloth soaked in neutral detergent.

        '''),
        ('user', '''
        사용자의 질문에 context 만을 이용해 한국어로 답변해 주세요.

        question : {query}

        context : {context}
        ''')
    ])

    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )
    smart_oven = {'query' : RunnablePassthrough(), 'context' : indexing_phase} | prompt | model | StrOutputParser()

    return smart_oven.invoke(query)

