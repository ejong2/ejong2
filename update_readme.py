import requests
from bs4 import BeautifulSoup

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    latest_post = {}
    # 최신 포스트 리스트를 담고 있는 div 태그를 찾습니다.
    post_list_section = soup.find('div', class_='FlatPostCardList_block__VoFQe')
    if post_list_section:
        # 리스트 내의 첫 번째 포스트를 찾습니다.
        first_post_section = post_list_section.find('div', class_='FlatPostCard_block__a1qM7')
        if first_post_section:
            # 포스트의 URL을 찾습니다.
            post_link = first_post_section.find('a', class_='VLink_block__Uwj4P', href=True)
            if post_link:
                latest_post['url'] = post_link['href']

            # 포스트의 제목을 찾습니다.
            post_title = post_link.find('h2')
            if post_title:
                latest_post['title'] = post_title.text.strip()

            # 썸네일 이미지를 찾습니다.
            post_thumbnail = first_post_section.find('img', src=True)
            if post_thumbnail:
                latest_post['thumbnail'] = post_thumbnail['src']

            return latest_post

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
    else:
        blog_post_content = "최신 블로그 포스트가 없습니다. 나중에 다시 확인해주세요!\n"

    content.insert(start_index, blog_post_content)

    with open('README.md', 'w') as file:
        file.writelines(content)

latest_post = fetch_latest_post()
update_readme(latest_post)
