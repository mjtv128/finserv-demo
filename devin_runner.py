import os
import requests
import time 

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY")
BASE_URL = "https://api.devin.ai/v1/sessions"


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

def create_session(prompt, schema):
    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        json={
            "prompt": prompt,
            "structured_output_schema": schema
        }
    )

    response.raise_for_status()
    return response.json()["session_id"]

def wait_for_session(session_id, timeout=40, interval=2):
    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

    status_url = f"{BASE_URL}/{session_id}"
    elapsed = 0

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status_enum") == "finished":
            return data.get("structured_output")

    raise TimeoutError("Devin session did not finish in time.")


def classify_issue(title, body):
    prompt = f"""You are an AI engineering triage assistant.

    Issue Title:
    {title}

    Issue Description:
    {body}

    Respond ONLY in strict JSON:

    {{
      "difficulty": "easy | medium | hard | unsure",
      "automation_category": "safe | review-needed",
      "risk_level": "low | medium | high",
      "reason": "short explanation"
    }}
    """

    schema = {
        "type": "object",
        "properties": {
            "difficulty": {"type": "string"},
            "automation_category": {"type": "string"},
            "risk_level": {"type": "string"},
            "reason": {"type": "string"}
        },
        "required": ["difficulty", "automation_category", "risk_level", "reason"]
    }

    return devin_structured_call(prompt, schema)
  
def devin_structured_call(prompt, schema):
    session_id = create_session(prompt, schema)
    return wait_for_session(session_id)

if __name__ == "__main__":
    print("🚀 Starting backlog scan...\n")

    issues = fetch_open_issues()

    print(f"Found {len(issues)} open issues.\n")

    for issue in issues:
      number = issue["number"]
      title = issue["title"]
      body = issue.get("body") or ""
      

      print(f"\nClassifying issue #{number}: {title}")

      
      result = classify_issue(title, body)

      # result = classify_issue(title, issue.get("body", ""))

      print("Raw classification result:", result)