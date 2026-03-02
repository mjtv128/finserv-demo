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


def get_issue_labels(issue_number):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}/labels"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return [label["name"] for label in response.json()]


def set_devin_status(issue_number, new_status):
    """
    Ensures only one devin-status:* label exists.
    """

    current_labels = get_issue_labels(issue_number)

    for label in current_labels:
        if label.startswith("devin-status:"):
            remove_label(issue_number, label)

    label_issue(issue_number, f"devin-status: {new_status}")

def pr_exists(issue_number):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls"
    params = {"state": "open", "per_page": 100}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()

    prs = response.json()

    branch_prefix = f"devin/issue-{issue_number}"

    for pr in prs:
        head_branch = pr["head"]["ref"]
        if head_branch.startswith(branch_prefix):
            return True

    return False
  
def branch_exists(issue_number):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/branches"
    params = {"per_page": 100}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()

    branches = response.json()

    branch_prefix = f"devin/issue-{issue_number}"

    for branch in branches:
        if branch["name"].startswith(branch_prefix):
            return True

    return False
  
def status_is_completed(issue_number):
    labels = get_issue_labels(issue_number)
    return "devin-status: completed" in labels

def send_slack(message):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return
    requests.post(webhook_url, json={"text": message})

# def count_open_devin_prs():
#     url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls"
#     params = {"state": "open", "per_page": 100}

#     response = requests.get(url, headers=HEADERS, params=params, timeout=20)
#     response.raise_for_status()

#     prs = response.json()

#     count = 0
#     for pr in prs:
#         labels = [l["name"] for l in pr.get("labels", [])]
#         if "devin-generated" in labels:
#             count += 1

#     return count

# def get_default_branch_sha():
#     # Get repo info
#     repo_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"
#     repo_response = requests.get(repo_url, headers=HEADERS, timeout=20)
#     repo_response.raise_for_status()

#     repo_data = repo_response.json()
#     default_branch = repo_data["default_branch"]

#     # Get branch reference
#     ref_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/git/ref/heads/{default_branch}"
#     ref_response = requests.get(ref_url, headers=HEADERS, timeout=20)
#     ref_response.raise_for_status()

#     sha = ref_response.json()["object"]["sha"]

#     return sha, default_branch
  
# def create_branch(branch_name, base_sha):
#     url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/git/refs"

#     response = requests.post(
#         url,
#         headers=HEADERS,
#         json={
#             "ref": f"refs/heads/{branch_name}",
#             "sha": base_sha
#         },
#         timeout=20
#     )
#     if response.status_code == 422:
#         # Branch already exists — safe to continue
#         return
#     response.raise_for_status()

# def create_or_update_file(path, content, branch, message):
#     url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/contents/{path}"

#     encoded_content = base64.b64encode(content.encode()).decode()

#     response = requests.put(
#         url,
#         headers=HEADERS,
#         json={
#             "message": message,
#             "content": encoded_content,
#             "branch": branch
#         },
#         timeout=20
#     )

#     response.raise_for_status()

# def create_draft_pr(title, body, head_branch, base_branch):
#     url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls"

#     response = requests.post(
#         url,
#         headers=HEADERS,
#         json={
#             "title": title,
#             "body": body,
#             "head": head_branch,
#             "base": base_branch,
#             "draft": True
#         },
#         timeout=20
#     )

#     response.raise_for_status()
#     return response.json()

def create_draft_pr(title, body, head_branch, base_branch):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls"

    response = requests.post(
        url,
        headers=HEADERS,
        json={
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch,
            "draft": True
        },
        timeout=20
    )

    print("PR RESPONSE STATUS:", response.status_code)
    print("PR RESPONSE BODY:", response.text)

    response.raise_for_status()
    return response.json()