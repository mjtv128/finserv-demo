import os
from devin_automation.devin_client import create_session, wait_for_session


def run_issue(issue):
    repo = os.environ.get("GITHUB_REPOSITORY")
    issue_number = issue["number"]

    prompt = f"""
You are an autonomous software engineer.

The repository below is connected via the Devin GitHub integration.
You have authenticated GitHub access to create branches and open pull requests.

Repository: https://github.com/{repo}

Fix GitHub issue #{issue_number}.

Issue Title:
{issue['title']}

Issue Body:
{issue.get('body', '')}

Instructions:

- Create branch: devin/issue-{issue_number}
- If branch exists, append a unique timestamp suffix.
- Implement the minimal correct fix.
- Do not modify unrelated files.
- Commit changes.
- Open a DRAFT pull request targeting the default branch.
- In the PR description include:
  - What the bug was
  - What the fix does
  - A short checklist for the human reviewer
- Reference and close issue #{issue_number} in the PR description using "Closes #{issue_number}".
- Post a comment on issue #{issue_number} saying: "🤖 Draft PR opened: [PR URL]"
- Do NOT merge the PR.
- Stop once the draft PR is successfully created.
"""

    session_id = create_session(prompt)
    return wait_for_session(session_id)