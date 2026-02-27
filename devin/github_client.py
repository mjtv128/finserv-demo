import os
import requests

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

BASE_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def fetch_open_issues(limit=20):
    response = requests.get(
        f"{BASE_URL}/issues",
        headers=HEADERS,
        params={"state": "open", "per_page": limit}
    )
    response.raise_for_status()
    return response.json()


def label_issue(issue_number, label):
    response = requests.post(
        f"{BASE_URL}/issues/{issue_number}/labels",
        headers=HEADERS,
        json={"labels": [label]}
    )
    response.raise_for_status()

def remove_label(issue_number, label_name):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels/{label_name}"
    response = requests.delete(url, headers=HEADERS)
    # GitHub returns 404 if label doesn't exist, which is fine
    if response.status_code not in (200, 204, 404):
        response.raise_for_status()
        
def post_comment(issue_number, body):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/comments"

    response = requests.post(
        url,
        headers=HEADERS,
        json={"body": body}
    )

    response.raise_for_status()