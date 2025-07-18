from answer_feedback import create_feedback_client, get_similar_negative_feedback, save_feedback_to_supabase
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils import extract_links
from web_crawling import get_dynamic_page_text
from web_search import search_serper_links

import os
import streamlit as st

load_dotenv()
supabase_client = create_feedback_client()

llm = ChatOpenAI(model="gpt-4.1", temperature=0.2) # GPT LLM 구성
memory = ConversationBufferMemory(return_messages=True) # 메모리 설정 (이전 대화 기억)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 한국 법률 전문가입니다. 사용자 질문을 바탕으로 법적 이슈를 분류하고, 실제 공공기관 정보를 활용해 해결 방법을 안내하세요."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{user_input}")
])
output_parser = StrOutputParser() # 출력 파서
chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_parser=StrOutputParser()) # LLMChain으로 대화형 챗 구성


issue_prompt = ChatPromptTemplate.from_messages([ # 이슈 분류용 프롬프트
    ("system", "다음 사용자의 문장은 어떤 법적 이슈에 해당하는지 한 단어 또는 짧은 문장으로 분류하세요. (예: 임금체불, 부당해고, 개인정보 유출 등)"),
    ("user", "{user_input}")
])
issue_chain = LLMChain( # 이슈 분류 LLMChain
    llm=ChatOpenAI(model="gpt-4.1", temperature=0.0),
    prompt=issue_prompt,
    output_parser=StrOutputParser()
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
            issue_type = issue_chain.run({"user_input": user_input}).strip()
            st.markdown(f"🧠 감지된 법적 이슈: **{issue_type}**")

            # 2️⃣ Serper 검색 (문제 유형 기반)
            SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # .env에서 불러오기
            query = f"{issue_type} 관련 신고 절차 site:moel.go.kr OR site:gov.kr OR site:minwon.go.kr"
            
            urls = search_serper_links(query, api_key=SERPER_API_KEY)
            first_url = urls[0] if urls else None

            # for url in urls: # 크롤링 후보군 디버깅용 UI
            #     st.markdown(f'크롤링 후보군: {url}')

            page_text = get_dynamic_page_text(first_url) if first_url else "[관련 페이지 없음]"

            # 3️⃣ GPT에게 해결 방안 요청
            feedback = get_similar_negative_feedback(supabase_client, user_input) # 이전에 부정적인 피드백이 있었는지 supabase 조회
            if feedback: # 있었다면
                prompt_extra = f"""
            과거 비슷한 질문에 대해 다음과 같은 GPT 응답이 있었고, 사용자는 이를 '부족하다'고 평가했습니다:

            질문: {feedback['question']}
            응답: {feedback['answer']}

            → 이번에는 더 구체적인 안내 (기관명, 신고 절차, 서류명 등)를 포함하여 다시 답변해주세요.
            """
                enriched_input = prompt_extra + "\n\n현재 사용자 질문: " + user_input
            else: # 없다면
                enriched_input = user_input

            # 최종 GPT 입력 구성
            combined_input = f"{enriched_input}\n\n[공공기관 본문 요약 참고]\n{page_text}"
            response = chain.run({"user_input": combined_input})

            # 🧾 GPT 답변 출력
            st.markdown(response)

            # 🔎 응답에서 링크 모두 추출 (마크다운 + 일반 URL + HTML 링크)
            urls = extract_links(response)
            if urls:
                with st.expander("🔗 관련 링크 보기"):
                    for url in urls[:3]:
                        st.markdown(f"- [{url}]({url})")
            else: st.info("🔗 GPT 응답에 링크가 포함되지 않았습니다.")
            
            with st.expander("📝 참고한 페이지 본문 보기"):
                st.markdown(f'참고한 페이지 링크: {first_url}')
                st.markdown(page_text if page_text else "_본문 없음_")
            
            # 사용자 평가 버튼
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍 도움이 되었어요", key="thumbs_up"):
                    st.success("감사합니다! 도움이 되었다니 기쁩니다.")
                    save_feedback_to_supabase(supabase_client, user_input, response, issue_type, "👍")
            with col2:
                if st.button("👎 부족했어요", key="thumbs_down"):
                    st.warning("죄송합니다. 더 나은 답변을 위해 개선하겠습니다.")
                    save_feedback_to_supabase(supabase_client, user_input, response, issue_type, "👎")

    # 세션 상태에 저장
    st.session_state.chat_history.append(("🧑‍💼 질문", user_input))
    st.session_state.chat_history.append(("🤖 GPT", response))