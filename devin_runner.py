import os
import requests

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def fetch_open_issues():
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {
        "state": "open",
        "per_page": 5
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("🚀 Starting backlog scan...\n")

    issues = fetch_open_issues()

    print(f"Found {len(issues)} open issues.\n")

    for issue in issues:
        print(f"- #{issue['number']} {issue['title']}")