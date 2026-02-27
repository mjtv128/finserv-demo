import os
import requests

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")

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

def classify_issue(title, body):
    url = "https://api.devin.ai/v1/sessions"

    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are an AI engineering triage assistant working on a large financial services monorepo.
    Your task is to evaluate a GitHub issue and classify it for automation readiness.

    Issue Title:
    {title}

    Issue Description:
    {body}

    Evaluate the issue across the following dimensions:

    1. difficulty
      - "easy"   → small bug, localized change, likely 1–2 files
      - "medium" → bounded change, may touch multiple files but not architectural
      - "hard"   → complex change, cross-cutting logic or significant refactor
      - "unsure" → insufficient information to determine scope

    2. automation_category
      - "safe" → likely safe for automated patch generation with human review
      - "review-needed" → requires human inspection before automation attempts

    3. risk_level
      - "low"    → minimal business or system impact
      - "medium" → moderate impact, some financial or logic sensitivity
      - "high"   → high business, compliance, or architectural risk

    Respond ONLY in strict JSON format:

    {{
      "difficulty": "easy | medium | hard | unsure",
      "automation_category": "safe | review-needed",
      "risk_level": "low | medium | high",
      "reason": "short explanation"
    }}

    Do not include markdown.
    Do not include extra commentary.
    Return valid JSON only.
    """

    response = requests.post(
        url,
        headers=headers,
        json={"prompt": prompt}
    )

    response.raise_for_status()
    data = response.json()

    print("Devin raw response:", data)  # TEMPORARY — for debugging

    return data

if __name__ == "__main__":
    print("🚀 Starting backlog scan...\n")

    issues = fetch_open_issues()

    print(f"Found {len(issues)} open issues.\n")

    for issue in issues:
      number = issue["number"]
      title = issue["title"]

      print(f"\nClassifying issue #{number}: {title}")
      body = issue.get("body") or ""
      result = classify_issue(title, body)

      # result = classify_issue(title, issue.get("body", ""))

      print("Raw classification result:", result)