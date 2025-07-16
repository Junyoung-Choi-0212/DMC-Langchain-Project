from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chains import ConversationChain
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import re
import streamlit as st

load_dotenv()

# 사용자의 input을 기준으로 검색할 tool 세팅
search_tool = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="web_search",
        func=search_tool.run,
        description="사용자의 법률 질문과 관련된 공공기관 웹 정보를 검색합니다."
    )
]

llm = ChatOpenAI(model="gpt-4.1", temperature=0.2) # GPT LLM 구성
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
st.set_page_config(page_title="법률 상담 챗봇", layout="wide")
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
            # 1️⃣ GPT로 법적 이슈 분류
            issue_classification_prompt = f"""
            다음 문장은 어떤 법적 문제에 해당합니까?
            가능한 분류 중 정확히 하나만 골라주세요:

            분류: 임금체불, 부당해고, 개인정보 유출, 계약서 미작성, 명예훼손, 가정폭력, 기타

            문장: {user_input}
            """
            issue_type_msg = llm.invoke(issue_classification_prompt)
            issue_type = issue_type_msg.content.strip() 
            st.markdown(f"🧠 감지된 법적 이슈: **{issue_type}**")

            # 2️⃣ DuckDuckGo 검색 (문제 유형 기반)
            query = f"{issue_type} 관련 신고 절차 site:moel.go.kr OR site:gov.kr OR site:minwon.go.kr"
            search_result = search_tool.run(query)

            # 3️⃣ GPT에게 해결 방안 요청
            final_prompt = f"""
            감지된 법적 이슈: {issue_type}

            사용자의 질문: {user_input}

            다음은 해당 이슈에 대한 공식 문서 검색 결과입니다:
            {search_result}

            위 정보를 바탕으로, 법률 전문가로서 해결 방법을 안내하세요.
            (기관명, 해결 절차, 제출 서류, 신고 링크 등 포함)
            """
            response = conversation.predict(input=final_prompt)

            # 🧾 GPT 답변 출력
            st.markdown(response)

            # 🔎 응답에서 링크 모두 추출 (마크다운 + 일반 URL + HTML 링크)
            markdown_urls = re.findall(r'\[[^\]]+\]\((https?://[^\s)]+)\)', response) # 1. 마크다운 링크 (ex: [text](url))
            plain_urls = re.findall(r'(?<!\])(?<!\))https?://[^\s)\]]+', response) # 2. 일반 링크 (띄어쓰기 구분된 텍스트 내 URL)
            html_urls = re.findall(r'href=[\'"]?(https?://[^\s\'">]+)', response) # 3. HTML 링크
            urls = list(set(markdown_urls + plain_urls + html_urls)) # 모두 합치고 중복 제거
            if urls:
                with st.expander("🔗 관련 링크 보기"):
                    for url in urls[:3]:
                        st.markdown(f"- [{url}]({url})")
            else: st.info("🔗 GPT 응답에 링크가 포함되지 않았습니다.")

            with st.expander("🔍 검색 결과 보기"): # 검색 결과 보기 (숨김 가능)
                st.markdown(search_result)

    # 세션 상태에 저장
    st.session_state.chat_history.append(("🧑‍💼 질문", user_input))
    st.session_state.chat_history.append(("🤖 GPT", response))