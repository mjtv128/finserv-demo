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


def run_issue(issue):
    repo = os.environ.get("GITHUB_REPOSITORY")
    issue_number = issue["number"]

    prompt = f"""
You are an autonomous software engineer.

Repository: https://github.com/{repo}

Fix GitHub issue #{issue_number}.

Issue Title:
{issue['title']}

Issue Body:
{issue.get('body', '')}

Instructions:
1. Clone the repository.
2. Create a new branch named: devin/issue-{issue_number}
3. Implement the fix.
4. Commit changes.
5. Open a DRAFT pull request targeting the default branch.
6. Reference issue #{issue_number} in the PR description.
7. Return the PR URL.
"""

    session_id = create_session(prompt, EXECUTION_SCHEMA)
    result = wait_for_session(session_id)

    return result