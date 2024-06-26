from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# 잘못된 패키지명을 수정합니다.
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_latest_post():
    url = 'https://velog.io/@enamu/posts'

    # 헤드리스 모드에서 실행하도록 ChromeOptions를 설정합니다.
    options = Options()
    options.add_argument("--headless")

    # ChromeDriverManager를 사용하여 ChromeDriver를 자동으로 다운로드하고, 설치된 드라이버의 경로를 사용합니다.
    # 이 부분이 수정되어야 합니다.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 기다립니다.
    time.sleep(5)

    # BeautifulSoup 객체를 생성합니다.
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'FlatPostCard_block__a1qM7' 클래스를 가진 div 태그를 찾습니다.
    post_block = soup.find('div', class_='FlatPostCard_block__a1qM7')

    # 썸네일 이미지 URL을 추출합니다.
    thumbnail_url = post_block.find('img')['src']

    # 게시글 제목을 추출합니다.
    title = post_block.find('h2').text

    # 게시글 URL을 추출합니다.
    post_url = post_block.find('a')['href']

    # WebDriver를 닫습니다.
    driver.quit()

    return {'thumbnail': thumbnail_url, 'title': title, 'url': post_url}

def update_readme(post):
    with open('README.md', 'r') as file:
        content = file.readlines()

    start_index = None
    end_index = None
    for idx, line in enumerate(content):
        if '[//]: # (latest_post)' in line:
            start_index = idx + 1
            continue
        if start_index and '</div><br/>' in line:
            end_index = idx
            break

    if start_index and end_index:
        del content[start_index:end_index+1]

    if post:
        thumbnail_tag = f"<img src='{post['thumbnail']}' alt='{post['title']}' width='150'/>\n"
        blog_post_content = (
            f"<div style='display: flex; align-items: center;'>\n"
            f"    <a href='{post['url']}'>\n"
            f"        {thumbnail_tag}"
            f"    </a>\n"
            f"    <div style='margin-left: 20px;'>\n"
            f"        <a href='{post['url']}' style='text-decoration: none; color: black; font-size: 18px;'>{post['title']}</a>\n"
            f"    </div>\n"
            f"</div><br/>\n"
        )
    else:
        blog_post_content = "최신 블로그 포스트가 없습니다. 나중에 다시 확인해주세요!\n"

    content.insert(start_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

latest_post = fetch_latest_post()
update_readme(latest_post)
