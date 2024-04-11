import requests
from bs4 import BeautifulSoup
import sys  # sys 모듈 추가

def fetch_latest_post():
    url = 'https://velog.io/@enamu/posts'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching the URL: {url}\n{e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        latest_post_section = soup.find('div', class_='FlatPostCard_block__a1qM7')
        if not latest_post_section:
            raise Exception("Latest post section not found.")

        latest_post = {}
        title_section = latest_post_section.find('h2')
        post_link = latest_post_section.find('a', class_='VLink_block__Uwj4P', href=True)
        thumbnail_section = latest_post_section.find('img', src=True)

        if title_section:
            latest_post['title'] = title_section.text.strip()
        else:
            raise Exception("Post title not found.")

        if post_link:
            latest_post['url'] = post_link['href']
        else:
            raise Exception("Post URL not found.")

        if thumbnail_section:
            latest_post['thumbnail'] = thumbnail_section['src']
        else:
            raise Exception("Post thumbnail not found.")

        return latest_post
    except Exception as e:
        print(f"An error occurred while parsing the webpage: {e}")
        return None

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
