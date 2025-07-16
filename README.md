# DMC-Langchain-Project
Langchain 개인 프로젝트 - 🧑‍⚖️ 법률 챗봇 (LangChain + GPT)

- [x]  github을 활용한 프로젝트 관리
  → 전체 프로젝트를 GitHub 기반으로 버전 관리하며 `.env`, `.py` 모듈, Streamlit UI, LangChain 구성을 모듈화하여 커밋 히스토리 관리.
- [x]  문제 정의에서 시작하는 프로젝트 시작
  → "임금체불", "부당해고", "가정폭력" 등 사용자의 다양한 법률 질문에 대해 적절한 **대응 방법 안내**가 필요하다는 문제를 정의하고 시작.
- [x]  배웠던 RAG에 다양한 기술, 스킬
  → GPT를 단순 질의응답이 아닌 RAG(Retrieval Augmented Generation) 구조로 사용.  
    - `Serper.dev` API를 활용해 `.go.kr` 공공기관 웹문서를 검색  
    - `Selenium` 기반 크롤링으로 동적 페이지 본문을 추출  
    - LangChain의 `ChatOpenAI`, `PromptTemplate`, `ConversationChain` 구성  
    - 검색 결과 + 사용자 질문 + 크롤링 본문을 GPT에게 통합 전달 → 해결책 생성
- [x]  문제 정의 → RAG → 해결
  → 전체 구조를 `문제 정의 → 자동 이슈 분류(GPT) → 공공문서 검색(Serper) → 본문 수집(Selenium) → GPT 요약` 흐름으로 완성.  
    Streamlit 기반 UI로 사용자 입력을 받고, GPT 답변을 말풍선 UI + 링크 + 본문 확인으로 구성.