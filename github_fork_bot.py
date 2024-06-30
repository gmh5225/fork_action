import requests
import schedule
import time
import os

# GitHub username and Personal Access Token
USERNAME = 'gmh5225'
# Set the GITHUB_TOKEN_FOR_BOT environment variable
TOKEN = os.getenv('GITHUB_TOKEN_FOR_BOT')

# List of keywords you are interested in
KEYWORDS = ['anti cheat', 'LLVM']

def search_repositories():
    headers = {
        'Authorization': f'token {TOKEN}'
    }
    repositories = []

    for keyword in KEYWORDS:
        url = f'https://api.github.com/search/repositories?q={keyword}&sort=updated&order=desc'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check response status code
            results = response.json().get('items', [])
            repositories.extend(results)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch repositories for keyword: {keyword}. Error: {e}")

    return repositories

def fork_repository(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/forks'
    headers = {
        'Authorization': f'token {TOKEN}'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print(f'Successfully forked {owner}/{repo}')
    else:
        print(f'Failed to fork {owner}/{repo}')


def main():
    repositories = search_repositories()
    for repo in repositories:
        owner = repo['owner']['login']
        if owner == USERNAME:
            continue
        repo_name = repo['name']
        print(f'Processing https://github.com/{owner}/{repo_name}')
        fork_repository(owner, repo_name)
        time.sleep(3)

while True:
    main()
    time.sleep(60)
