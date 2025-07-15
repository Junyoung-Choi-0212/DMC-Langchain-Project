from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import streamlit as st

load_dotenv()

llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.2) # GPT LLM 구성
memory = ConversationBufferMemory(return_messages=True) # 메모리 설정 (이전 대화 기억)
prompt = ChatPromptTemplate.from_template("""
당신은 한국의 법률 상담 도우미입니다. 
아래는 지금까지의 대화입니다:

{history}

---

현재 사용자 질문:
{input}

법적 이슈를 분류하고, 구체적인 해결 방안을 설명해주세요 (기관명, 절차, 필요서류, 제출링크 등).
""")
output_parser = StrOutputParser() # 출력 파서

# ConversationChain으로 대화형 챗 구성
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    output_parser=output_parser,
    verbose=True
)

# Streamlit 앱
st.markdown("## 🧑‍⚖️ 법률 챗봇 (LangChain + GPT)")

# 대화 입력
user_input = st.chat_input("질문을 입력하세요...")

# 대화 히스토리 출력
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "🧑‍💼 질문" else "assistant"):
        st.markdown(msg if role != "🧑‍💼 질문" else f"**{msg}**")

# 입력이 있는 경우 → 답변 받고 출력
if user_input:
    with st.chat_message("user"):
        st.markdown(f"**{user_input}**")

    with st.chat_message("assistant"):
        with st.spinner("GPT가 해결 방안을 분석 중입니다..."):
            response = conversation.predict(input=user_input)
            st.markdown(response)

    # 세션 상태에 저장
    st.session_state.chat_history.append(("🧑‍💼 질문", user_input))
    st.session_state.chat_history.append(("🤖 GPT", response))