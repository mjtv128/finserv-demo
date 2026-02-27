import os
import requests

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def fetch_open_issues(limit=20):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues"
    params = {
        "state": "open",
        "per_page": limit
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def label_issue(issue_number, label):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels"
    response = requests.post(url, headers=HEADERS, json={"labels": [label]})
    response.raise_for_status()


def get_issue_labels(issue_number):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return [label["name"] for label in response.json()]


def remove_label(issue_number, label_name):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels/{label_name}"
    response = requests.delete(url, headers=HEADERS)

    # 404 just means label wasn't there — safe to ignore
    if response.status_code not in (200, 204, 404):
        response.raise_for_status()


def post_comment(issue_number, body):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/comments"
    response = requests.post(url, headers=HEADERS, json={"body": body})
    response.raise_for_status()