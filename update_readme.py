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
        content = file.read()

    # README에 업데이트할 내용을 추가
    updated_content = content + f"\nLatest blog post: [{post['title']}]({post['url']})"

    with open('README.md', 'w') as file:
        file.write(updated_content)

latest_post = fetch_latest_post()
update_readme(latest_post)
