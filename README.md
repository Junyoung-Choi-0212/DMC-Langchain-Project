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
- 사용자는 답변에 대해 👍/👎 평가를 남길 수 있으며, 해당 피드백은 Supabase에 자동 저장
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
6. 사용자는 GPT의 응답에 대해 👍 또는 👎 평가를 남길 수 있으며,
   해당 피드백은 Supabase에 저장되어 추후 응답 품질 개선에 활용됩니다.

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

- 주소 변경 신고는 어디서 하나요?

- 주민등록증 재발급은 온라인으로 할 수 있나요?

- 주민센터에서 개인정보가 유출됐는데 어디에 신고하죠?

- 전입신고를 안 했을 때 불이익이 있나요?

- 방치된 차량을 신고하고 싶은데 어떤 절차가 있나요?

## 시연 영상
아래 이미지를 클릭하면 YouTube에서 시연 영상을 확인할 수 있습니다:

[![영상 제목](https://img.youtube.com/vi/2Wz8JQdL-Jg/0.jpg)](https://www.youtube.com/watch?v=2Wz8JQdL-Jg)

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
SUPABASE_URL=your_key_here
SUPABASE_KEY=your_key_here
```
4. 실행
```bash
streamlit run app.py
```
5. Supabase 테이블 구성

Streamlit 앱은 사용자 피드백 데이터를 Supabase DB에 저장합니다.  
앱 실행 전, 다음과 같이 `feedback` 테이블을 생성하세요.

### ✅ 테이블 생성 방법

1. Supabase 프로젝트에 접속 → `Table Editor` 클릭
2. `New Table` → 이름: `feedback`
3. 다음과 같이 컬럼을 추가하고 저장합니다:

| 컬럼명       | 타입        | 옵션                                           |
|--------------|-------------|------------------------------------------------|
| `id`         | int8        | Primary Key ✅, Is Identity ✅, Is Unique ✅     |
| `question`   | text        | 질문 내용                                     |
| `answer`     | text        | GPT가 생성한 답변                             |
| `issue_type` | text        | GPT가 분류한 법적 이슈 (예: 임금체불)         |
| `feedback`   | text        | 사용자 평가 (`👍` 또는 `👎`)                  |
| `created_at` | timestamp   | 기본값: `now()`                                |

> 💡 **주의:** 테이블 생성 시 `Schema`는 반드시 `public`으로 설정하세요.  
> `storage` 스키마는 일반 사용자가 접근 권한이 없어 오류가 발생합니다.

### ✅ Supabase RLS(Row-Level Security) 설정
피드백을 Supabase에 정상적으로 저장하려면 `feedback` 테이블의 RLS(Row-Level Security) 설정을 반드시 확인해야 합니다.

#### 🔹 옵션 1: RLS 비활성화 (개발/테스트 환경용)
- Supabase 콘솔에서 `feedback` 테이블 선택  
- 상단 메뉴에서 **RLS** → `Disable RLS` 클릭  
- 누구나 삽입 가능 (테스트 환경에만 권장)

#### 🔹 옵션 2: RLS 활성화 상태에서 삽입 허용 정책 추가 (운영 환경 권장)
RLS를 활성화한 경우, 다음과 같이 삽입 허용 정책을 추가해야 합니다:
```sql
CREATE POLICY "Allow insert from all"
  ON public.feedback
  FOR INSERT
  TO public
  USING (true);
```
- Supabase Console > `feedback` 테이블 > **Auth** 탭 > `Create Policy` 클릭  
- 위 SQL을 입력 후 저장

> ⚠️ 정책이 없거나 Supabase 키가 잘못된 경우 다음과 같은 오류가 발생할 수 있습니다:

```pgsql
new row violates row-level security policy for table "feedback"
```

#### 🧩 삽입 실패 시 체크리스트
✅ 아래 항목들을 하나씩 확인하세요:
- [ ] Supabase 키로 **anon(public)** 키를 사용하고 있는가?
- [ ] 컬럼명은 `question`, `answer`, `issue_type`, `feedback` 과 정확히 일치하는가?
- [ ] RLS가 활성화되어 있고, 위 정책이 존재하는가?
- [ ] 정책의 대상이 `TO public USING (true)` 로 설정되어 있는가?

## 프로젝트 체크리스트
- [x]  Github을 활용한 프로젝트 관리
  → 전체 프로젝트를 GitHub 기반으로 버전 관리하며 `.env`, `.py` 모듈, Streamlit UI, LangChain 구성을 모듈화하여 커밋 히스토리 관리.
- [x]  문제 정의에서 시작하는 프로젝트 시작
  → "임금체불", "부당해고", "가정폭력" 등 사용자의 다양한 법률 질문에 대해 적절한 **대응 방법 안내**가 필요하다는 문제를 정의하고 시작.
- [x]  배웠던 RAG에 다양한 기술, 스킬
  → GPT를 단순 질의응답이 아닌 RAG(Retrieval Augmented Generation) 구조로 사용.  
    - `Serper.dev` API를 활용해 `.go.kr` 공공기관 웹문서를 검색  
    - `Selenium` 기반 크롤링으로 동적 페이지 본문을 추출  
    - LangChain의 `ChatOpenAI`, `PromptTemplate`, `LLMChain` 구성  
    - 검색 결과 + 사용자 질문 + 크롤링 본문을 GPT에게 통합 전달 → 해결책 생성
- [x]  문제 정의 → RAG → 해결
  → 전체 구조를 `문제 정의 → 자동 이슈 분류(GPT) → 공공문서 검색(Serper) → 본문 수집(Selenium) → GPT 요약` 흐름으로 완성.  
    Streamlit 기반 UI로 사용자 입력을 받고, GPT 답변을 말풍선 UI + 링크 + 본문 확인으로 구성.

## 프로젝트 학습 포인트
- LangChain과 GPT를 활용한 RAG 구조를 처음부터 직접 구성
- 다양한 법률 분야에 대응 가능한 이슈 분류 시스템 설계
- Serper API + Selenium을 연계한 실시간 웹 문서 기반 답변 생성
- 사용자 중심의 Streamlit 챗봇 UI 설계 및 상태 관리 구현
- 사용자 피드백(👍/👎)을 수집하고, 이를 향후 응답 품질 개선에 반영하는 구조 설계

## 향후 확장 아이디어
- 피드백 통계 시각화 (Streamlit에서 평가 결과 차트로 표시)
- 사용자 의견 수집 필드 (이유 입력: “링크가 없음”, “설명이 부족함” 등)
- GPT 개선 예시 자동 생성: 유사 질문에 더 나은 답변 예측
- 사용자별 피드백 조회 (로그인 기반 확장 시)

## ✅ 상세 기술 스택
| 기술명                     | 버전       | 설명 |
|--------------------------|------------|------|
| BeautifulSoup            | v4.13.4    | 동적 웹페이지의 HTML 파싱 및 본문 텍스트 추출 |
| LangChain                | v0.3.26    | GPT 호출, 프롬프트 관리, 체인 구성 등 핵심 로직 |
| OpenAI                   | v1.30.1    | 자연어 처리 및 요약 생성 LLM |
| pipreqs                  | v0.5.0     | 실행을 위한 `requirements.txt` 자동 생성 (`pipreqs . --force`) |
| python-dotenv            | v1.1.1     | API 키 및 환경 변수 관리 |
| Python                   | v3.12.11   | 전체 백엔드 및 LLM 처리 |
| Selenium                 | v4.34.2    | 동적 웹페이지 크롤링 자동화 |
| Serper.dev API           | -          | `.go.kr` 공식 문서 검색 (Google 기반) |
| Streamlit                | v1.47.0    | 사용자 인터페이스 구성 (chat UI, 입력창, 말풍선 등) |
| Supabase                 | v2.17.0    | 피드백(질문, 응답, 이슈 분류, 평가 결과)을 클라우드 DB에 저장 |
| webdriver-manager        | v4.0.2     | 크롬 드라이버 자동 설치 및 관리 |


## 참고 문서
- [GPT API 공식 문서](https://platform.openai.com/docs/overview)
- [LangChain Docs](https://docs.langchain.com/)
- [Serper API 공식 문서](https://serper.dev/docs)
- [Supabase Docs](https://supabase.com/docs)
