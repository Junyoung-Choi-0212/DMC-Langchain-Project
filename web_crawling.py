from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_dynamic_page_text(url, max_chars=2000):
    try:
        # 브라우저 옵션 설정
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # ✅ Chrome 드라이버 서비스 설정
        service = Service(ChromeDriverManager().install())

        # ✅ WebDriver 객체 생성 (최신 방식)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # 본문 추출 영역
        main = (
            soup.find(id="content") or
            soup.find("main") or
            soup.find("article") or
            soup.find("section") or
            soup
        )
        text = main.get_text(separator="\n", strip=True)
        print("🧪 추출된 원본 본문:\n", text[:1000])  # 처음 1000자만
        print("▶ 추출 대상 태그:", main.name)
        print("▶ 추출된 text 길이:", len(text))

        lines = text.splitlines()
        clean_text = "\n".join(lines)

        return clean_text[:max_chars] if clean_text else "[본문 없음]"

    except Exception as e:
        return f"[동적 페이지 크롤링 실패: {e}]"