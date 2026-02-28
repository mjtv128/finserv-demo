# devin/devin_worker.py

import os
from devin.devin_client import create_session, wait_for_session


EXECUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "files_changed": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "new_code": {"type": "string"}
                },
                "required": ["file_path", "new_code"]
            }
        }
    },
    "required": ["summary", "files_changed"]
}


def run_issue(issue):
    repo = os.environ.get("GITHUB_REPOSITORY")
    issue_number = issue["number"]

    prompt = f"""
You are a software engineer.

Repository: https://github.com/{repo}

Fix GitHub issue #{issue_number}.

Issue Title:
{issue['title']}

Issue Body:
{issue.get('body', '')}

Return structured JSON only:

{
  "summary": "short explanation of fix",
  "files_changed": [
    {
      "file_path": "path/to/file.py",
      "new_code": "full updated file content"
    }
  ]
}
"""

    session_id = create_session(prompt, EXECUTION_SCHEMA)
    return wait_for_session(session_id)