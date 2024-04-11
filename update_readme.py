import requests
from bs4 import BeautifulSoup
import sys  # sys 모듈 추가

def fetch_latest_post():
    url = 'https://velog.io/@enamu/posts'
    try:
        response = requests.get(url)
        # 웹 페이지 로드 실패 시 에러 처리
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 최신 포스트의 컨테이너 추출
        posts_container = soup.find('div', class_='FlatPostCardList_block__VoFQe')
        if not posts_container:
            raise ValueError("Posts container not found")

        # 최신 포스트의 세부 정보 추출
        latest_post_card = posts_container.find('div', class_='FlatPostCard_block__a1qM7')
        if not latest_post_card:
            raise ValueError("Latest post not found")

        post_link = latest_post_card.find('a', class_='VLink_block__Uwj4P')['href']
        post_title = latest_post_card.find('h2').text.strip()
        post_thumbnail = latest_post_card.find('img', src=True)['src']

        return {
            'url': post_link,
            'title': post_title,
            'thumbnail': post_thumbnail
        }
    except Exception as e:
        print(f"Error parsing the webpage: {e}")
        return None

latest_post = fetch_latest_post()
if latest_post:
    print("Latest Post Details:")
    print(f"Title: {latest_post['title']}")
    print(f"URL: {latest_post['url']}")
    print(f"Thumbnail: {latest_post['thumbnail']}")
else:
    print("Failed to fetch the latest blog post.")

def update_readme(post):
    if post is None:
        # 변경된 부분: 에러 메시지를 README에 쓰는 대신, 에러 로그를 출력하고 프로그램 종료
        sys.exit("Failed to fetch or parse the latest blog post. Exiting the script.")

    with open('README.md', 'r') as file:
        content = file.readlines()

    start_index, end_index = None, None
    for idx, line in enumerate(content):
        if '[//]: # (latest_post)' in line:
            start_index = idx + 1
            continue
        if start_index and '</div><br/>' in line:
            end_index = idx
            break

    if start_index is not None and end_index is not None:
        del content[start_index:end_index+1]

    thumbnail_tag = f"<img src='{post['thumbnail']}' alt='{post['title']}' width='150'/>\n" if 'thumbnail' in post else ""
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
    content.insert(start_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

latest_post = fetch_latest_post()
update_readme(latest_post)
