# devin/devin_worker.py

import os
from devin.devin_client import create_session, wait_for_session


EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "analysis": {"type": "string"},
        "proposed_fix": {"type": "string"}
    },
    "required": ["analysis", "proposed_fix"]
}


def run_issue(issue):
    repo = os.environ.get("GITHUB_REPOSITORY")
    issue_number = issue["number"]

    prompt = f"""
You are a senior software engineer reviewing a GitHub issue.

Repository: https://github.com/{repo}

Issue #{issue_number}

Title:
{issue['title']}

Body:
{issue.get('body', '')}

Do NOT implement code.
Do NOT clone the repo.
Do NOT create branches.

Just analyze the issue and explain:

1. What is causing the bug?
2. What exact code change should be made?
3. What file is likely affected?

Return structured JSON only:

{{
  "analysis": "clear explanation of root cause",
  "proposed_fix": "precise description of code change"
}}
"""

    session_id = create_session(prompt, EXECUTION_SCHEMA)
    return wait_for_session(session_id)