import requests
from bs4 import BeautifulSoup

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    latest_post = {}
    # 웹 페이지 구조에 따른 수정된 선택자 사용
    latest_post_section = soup.find('div', class_='FlatPostCard_block__a1qM7')
    if latest_post_section:
        title_section = latest_post_section.find('h2')
        if title_section:
            latest_post['title'] = title_section.text.strip()
        else:
            print("Title not found")
            return None

        # URL을 찾는 방식 수정
        post_link = latest_post_section.find('a', class_='VLink_block__Uwj4P', href=True)
        if post_link:
            latest_post['url'] = post_link['href']
        else:
            print("Post URL not found")
            return None

        # 썸네일 찾기
        thumbnail_section = latest_post_section.find('img', src=True)
        if thumbnail_section:
            latest_post['thumbnail'] = thumbnail_section['src']
        else:
            print("Thumbnail not found")
            return None

        return latest_post
    else:
        print("Latest post section not found")
        return None

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
