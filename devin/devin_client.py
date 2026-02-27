import os
import requests
import time

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")
BASE_URL = "https://api.devin.ai/v1/sessions"

HEADERS = {
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    "Content-Type": "application/json"
}


def create_session(prompt, schema):
    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json={
            "prompt": prompt,
            "structured_output_schema": schema
        }
    )
    response.raise_for_status()
    return response.json()["session_id"]


def wait_for_session(session_id, timeout=90, interval=2):
    elapsed = 0

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        response = requests.get(
            f"{BASE_URL}/{session_id}",
            headers=HEADERS
        )
        response.raise_for_status()

        data = response.json()
        if data.get("structured_output"):
            return data["structured_output"]

    raise TimeoutError("Devin session timed out.")

def count_open_devin_prs():
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls"
    params = {"state": "open", "per_page": 100}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()

    prs = response.json()

    return len([
        pr for pr in prs
        if any(label["name"] == "devin-generated" for label in pr.get("labels", []))
    ])

def fetch_executable_issues():
    issues = fetch_open_issues(limit=50)

    executable = []

    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", [])]

        if "devin-easy" in labels or "devin-medium" in labels:
            if "devin-in-progress" not in labels:
                executable.append(issue)

    return executable
  