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