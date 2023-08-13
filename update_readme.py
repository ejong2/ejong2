import requests

def fetch_latest_post():
    url = 'https://velog.io/@enamu'
    response = requests.get(url)
    # 여기에 JSON 응답에서 필요한 데이터를 추출하는 코드를 작성
    # 예제 응답을 참조하여 적절한 코드를 작성하세요
    latest_post = response.json()['latest_post']
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
