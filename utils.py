import re

def extract_links(target):
    markdown_urls = re.findall(r'\[[^\]]+\]\((https?://[^\s)]+)\)', target) # 1. 마크다운 링크 (ex: [text](url))
    plain_urls = re.findall(r'(?<!\])(?<!\))https?://[^\s)\]]+', target) # 2. 일반 링크 (띄어쓰기 구분된 텍스트 내 URL)
    html_urls = re.findall(r'href=[\'"]?(https?://[^\s\'">]+)', target) # 3. HTML 링크
    
    return list(set(markdown_urls + plain_urls + html_urls)) # 모두 합치고 중복 제거