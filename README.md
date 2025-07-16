# DMC-Langchain-Project
Langchain 개인 프로젝트 - 🧑‍⚖️ 법률 챗봇 (LangChain + GPT)

- [x]  github을 활용한 프로젝트 관리
  - Repository 생성 완료  
- [x]  문제 정의에서 시작하는 프로젝트 시작
  - 법적 분쟁에 익숙하지 않은 일반인이 적절한 대응을 하기 어려운 문제를 해결하기 위해, 고용노동부·국민신문고 등 공공기관의 절차 안내 및 문서 데이터를 수집·정리하고, 사용자 입력을 자연어 처리해 상황에 맞는 법적 대처 방안을 자동으로 추천하겠다.
- [x]  배웠던 RAG에 다양한 기술, 스킬
  - ChatOpenAI, ChatPromptTemplate, StrOutputParser, langchain.chains 등의 기술 활용
- [x]  문제 정의 → RAG → 해결
  - 문제 정의: 사용자 입력 -> 자연어 처리 -> 공공기관의 데이터를 수집·정리 -> 해결 방안 추천
  - RAG: 사용자 입력 -> GPT-4.1로 사용자가 물어본 케이스 자동 분류 -> DuckDuckGo 검색에 site:moel.go.kr 와 같은 제한을 줘 공공기관에서만 검색하게 처리 -> 사용자 질문 및 검색 결과 등을 종합해 GPT를 통해 답변 받기 -> 해결책 제시 및 ConversationChain으로 후속 질문이 가능하게 처리 
  - 해결: RAG 과정을 거쳐 사용자에게 해결 방안 제시 및 답변에 활용된 링크 및 검색 내역을 선택적으로 보여줄 수 있게 Streamlit의 expander로 처리