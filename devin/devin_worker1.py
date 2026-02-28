# devin/devin_worker.py

import os
from devin.devin_client import create_session, wait_for_session


EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "pr_url": {"type": "string"}
    },
    "required": ["status"]
}


def run_issue(issue, triage):
    repo = os.environ.get("GITHUB_REPOSITORY")
    issue_number = issue["number"]

    prompt = f"""
You are an autonomous software engineer operating within a controlled automation system.

Repository: https://github.com/{repo}

This issue has already been triaged.

Issue #{issue_number}

Title:
{issue['title']}

Body:
{issue.get('body', '')}

Triage Summary:
{triage['summary']}

Difficulty:
{triage['difficulty']}

Recommended Action:
{triage['recommended_action']}

Reasoning:
{triage['reasoning']}

Instructions:

- Only proceed if the issue is small-to-medium in scope.
- Create branch: devin/issue-{issue_number}
- Implement the fix.
- Keep changes minimal and targeted.
- Open a DRAFT pull request.
- Reference issue #{issue_number} in the PR description.
- Return the PR URL.
"""

    session_id = create_session(prompt, EXECUTION_SCHEMA)
    result = wait_for_session(session_id)

    return result