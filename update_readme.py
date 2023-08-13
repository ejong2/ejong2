import requests
from bs4 import BeautifulSoup

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 최신 포스트의 정보를 추출합니다.
    latest_post = {}
    latest_post_section = soup.find('div', {'class': 'sc-12sw3o5-4'}) # 적절한 클래스나 태그를 사용하세요
    latest_post['url'] = url + latest_post_section.find('a')['href']
    latest_post['thumbnail'] = latest_post_section.find('img')['src']
    latest_post['title'] = latest_post_section.find('h4').text

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
    blog_post_content = f"<a href='{post['url']}'>\n    <img src='{post['thumbnail']}' alt='{post['title']}'/>\n</a><br/>\n"
    
    # 삽입 위치에 블로그 포스트 내용 삽입
    content.insert(insert_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

latest_post = fetch_latest_post()
update_readme(latest_post)
