import requests
from bs4 import BeautifulSoup

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 최신 포스트의 정보를 추출합니다.
    latest_post = {}
    latest_post_section = soup.find('h2')  # 최신 포스트의 제목을 담고 있는 h2 태그를 찾습니다.
    if latest_post_section:
        latest_post['title'] = latest_post_section.text.strip()

        # 최신 포스트의 URL을 찾습니다. - 수정된 부분
        latest_post_url_section = latest_post_section.find_parent('a', href=True)
        if latest_post_url_section:
            latest_post['url'] = latest_post_url_section['href']

        # 썸네일 이미지를 찾습니다. - 수정된 부분
        latest_post_thumbnail_section = latest_post_section.find_parent('div').find('img', src=True)
        if latest_post_thumbnail_section:
            latest_post['thumbnail'] = latest_post_thumbnail_section['src']

        return latest_post

def update_readme(post):
    with open('README.md', 'r') as file:
        content = file.readlines()

    # 블로그 포스트를 삽입할 위치 찾기 및 기존 포스트 제거
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

    # 삽입할 블로그 포스트 내용 작성
    if post:  # 포스트가 있을 경우
        thumbnail_tag = (
            f"<img src='{post['thumbnail']}' alt='{post['title']}' width='150'/>\n" if 'thumbnail' in post else ""
        )
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
    else:  # 포스트가 없을 경우 대체할 내용
        blog_post_content = "최신 블로그 포스트가 없습니다. 나중에 다시 확인해주세요!\n"

    # 삽입 위치에 블로그 포스트 내용 삽입
    content.insert(start_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

latest_post = fetch_latest_post()
update_readme(latest_post)
