from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # webdriver_manager 패키지로부터 올바르게 임포트합니다.
import time

def fetch_latest_post():
    url = 'https://velog.io/@enamu/posts'

    # webdriver_manager를 사용하여 ChromeDriver를 자동으로 다운로드하고 경로를 가져옵니다.
    # ChromeDriverManager().install()은 필요한 ChromeDriver를 다운로드하고, 설치된 드라이버의 경로를 반환합니다.
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    post_block = soup.find('div', class_='FlatPostCard_block__a1qM7')
    thumbnail_url = post_block.find('img')['src']
    title = post_block.find('h2').text
    post_url = post_block.find('a')['href']

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
