import requests
from bs4 import BeautifulSoup

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 최신 포스트의 정보를 추출합니다.
    latest_post = {}
    latest_post_section = soup.find('h1') # 최신 포스트의 제목을 담고 있는 h1 태그를 찾습니다.
    latest_post['title'] = latest_post_section.text

    # 최신 포스트의 URL을 찾습니다. URL은 h1 태그의 부모 div 태그 내의 a 태그의 href 속성에 있습니다.
    latest_post_url_section = latest_post_section.find_parent('div').find('a', class_='sc-jQrDum')
    latest_post['url'] = latest_post_url_section['href']

    # 썸네일 이미지를 찾습니다. 이미지는 URL 섹션의 이전 div 태그 내에 있을 수 있습니다.
    latest_post_thumbnail_section = latest_post_section.find_previous_sibling('div').find('img')
    latest_post['thumbnail'] = latest_post_thumbnail_section['src']

    return latest_post

def update_readme(post):
    with open('README.md', 'r') as file:
        content = file.readlines()

    # 블로그 포스트를 삽입할 위치 찾기
    insert_index = None
    for idx, line in enumerate(content):
        if '[//]: # (latest_post)' in line:
            insert_index = idx + 1
            break

    # 삽입할 블로그 포스트 내용 작성
    if post:  # 포스트가 있을 경우
        blog_post_content = f"<a href='{post['url']}'>\n    <img src='{post['thumbnail']}' alt='{post['title']}'/>\n</a><br/>\n"
    else:  # 포스트가 없을 경우 대체할 내용
        blog_post_content = "최신 블로그 포스트가 없습니다. 나중에 다시 확인해주세요!\n"

    # 삽입 위치에 블로그 포스트 내용 삽입
    content.insert(insert_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

# 예시: 최신 포스트가 없을 경우 대체 내용 삽입
update_readme()

latest_post = fetch_latest_post()
update_readme(latest_post)
