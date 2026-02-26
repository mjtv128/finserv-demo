import os
import requests

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

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
  
def label_pr(issue_number, label):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels"
    response = requests.post(url, headers=HEADERS, json={"labels": [label]})
    response.raise_for_status()

if __name__ == "__main__":
    print("🚀 Starting backlog scan...\n")

    issues = fetch_open_issues()

    print(f"Found {len(issues)} open issues.\n")

    for issue in issues:
        number = issue["number"]
    title = issue["title"]

    print(f"Mock classifying issue #{number}: {title}")

    fixable = True

    if fixable:
      label_pr(number, "devinfix-candidate")
      print(f"→ Issue #{number} labeled as devinfix-candidate")