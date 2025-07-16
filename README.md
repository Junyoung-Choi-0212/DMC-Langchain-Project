# 🧑‍⚖️ DMC-Langchain-Project – 법률 문제 자동 분석 및 해결 도우미 (LangChain + GPT)

GPT와 LangChain, 공공기관 웹 검색을 활용해  
사용자가 자유롭게 입력한 법률 문제를 자동으로 분석하고,  
관련 공공기관(.go.kr) 문서에서 신고 절차, 제출 서류, 대응 기관 등 실무적인 해결 방법을 자동으로 찾아주는 법률 AI 상담 시스템입니다.

- 사용자의 질문을 GPT가 자동 분류 (예: 임금체불, 부당해고, 양육비 등)
- 관련 이슈에 맞는 공공기관 문서를 실시간 검색 (Serper.dev API 활용)
- Selenium을 활용해 해당 페이지의 실제 본문을 크롤링
- GPT가 사용자의 질문 + 본문 내용을 바탕으로 구체적인 해결책 안내

Streamlit 기반 UI를 통해 실제 챗봇 형태로 법률상 대처 방안을 직관적으로 제공합니다.

## 주요 기능 요약
- 자유로운 한국어 질문 입력 (예: 임금체불, 부당해고, 양육비 등)
- GPT-4를 통한 자동 이슈 분류 (질문을 바탕으로 법적 쟁점 추론)
- 공공기관(.go.kr) 문서 실시간 검색 (Serper API 활용)
- Selenium 기반 동적 웹 페이지 크롤링 → 실제 본문 추출
- GPT가 본문 + 사용자 질문을 종합하여 구체적인 해결 방안 생성
- 말풍선 형태의 대화형 UI (Streamlit 기반)
- 검색된 공공기관 문서 링크 및 본문 미리보기 제공

## 프로젝트 사용 예시(예상 동작 흐름)
1. 사용자가 입력: _"사장이 알바비를 두 달째 안 줘요"_
2. GPT가 해당 문장을 "임금체불" 이슈로 분류
3. 고용노동부, 민원포털 등 공공기관에서 `.go.kr` 도메인 기반 문서 검색
4. 해당 문서의 본문을 Selenium으로 크롤링하여 정제된 텍스트로 추출
5. GPT가 사용자 질문 + 본문을 종합하여, 다음과 같은 해결 방법을 생성:
> 💬 **GPT 응답 예시**  
> “고용노동부 노동포털에서 '임금체불 진정서'를 제출할 수 있습니다. 온라인 민원 접수 경로는 다음과 같습니다...”

## 예시 질문
**노동 관련**
- 사장이 두 달째 알바비를 안 주고 있어요  
- 갑자기 부당하게 해고당했는데 어떻게 해야 하나요?
**민사/계약**
- 전세보증금을 못 받고 이사 나왔어요
**형사/수사**
- 경찰 조사 받을 때 진술 거부해도 되나요?
**가정/양육**
- 아이 아빠가 양육비를 계속 안 줘요
**행정/개인정보**
- 주민센터에서 개인정보를 유출했는데 어디에 신고하죠?
**기타 민원**
• 주소 변경 신고는 어디서 하나요?
• 주민등록증 재발급은 온라인으로 할 수 있나요?
• 주민센터에서 개인정보가 유출됐는데 어디에 신고하죠?
• 전입신고를 안 했을 때 불이익이 있나요?
• 방치된 차량을 신고하고 싶은데 어떤 절차가 있나요?

## 프로젝트 실행 순서
1. Repository clone
```bash
git clone https://github.com/your-repo-name/DMC-Langchain-Project.git
cd DMC-Langchain-Project
```
2. 가상환경 구성 및 패키지 설치
```bash
pip install -r requirements.txt
```
3. .env 파일 생성
```bash
# .env 예시
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```
4. 실행
```bash
streamlit run app.py
```

## 프로젝트 체크리스트
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

## 프로젝트 학습 포인트
- LangChain과 GPT를 활용한 RAG 구조를 처음부터 직접 구성
- 다양한 법률 분야에 대응 가능한 이슈 분류 시스템 설계
- Serper API + Selenium을 연계한 실시간 웹 문서 기반 답변 생성
- 사용자 중심의 Streamlit 챗봇 UI 설계 및 상태 관리 구현

## 상세 기술 스택
- **Python(v3.12.11)**: 전체 백엔드 및 LLM 처리
- **Streamlit(v1.46.1)**: 사용자 인터페이스 구성 (chat UI, 입력창, 말풍선 등)
- **LangChain(v0.3.26)**: GPT 호출, 프롬프트 관리, 체인 구성 등 핵심 로직
- **OpenAI(v1.30.1)**: 자연어 처리 및 요약 생성 LLM
- **Serper.dev API**: `.go.kr` 공식 문서 검색 (Google 기반)
- **Selenium(v4.34.2) + BeautifulSoup(v4.13.4)**: 동적 웹페이지 크롤링 및 본문 텍스트 추출
- **python-dotenv(v1.1.1)**: API 키 및 환경 변수 관리
- **webdriver-manager(v4.0.2)**: 크롬 드라이버 자동 설치 및 관리
- **pipreqs(v0.5.0)**: 추후 실행을 위한 requirements.txt를 제작하는데 사용(pipreqs . --force)

## 참고 문서
- [Serper API 공식 문서](https://serper.dev/docs)
- [LangChain Docs](https://docs.langchain.com/)
- [GPT API 공식 문서](https://platform.openai.com/docs/overview)