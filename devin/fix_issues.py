# devin/fix_issues.py

from devin.github_client import fetch_open_issues
from devin.issue_runner import execute_issue
import os

def run_execution_cycle():
    print("🚀 Starting execution cycle")
    label = os.environ.get("ISSUE_LABEL", "")
    if label and label != "devin-fix":
        return

    issues = fetch_open_issues(limit=10)

    if not issues:
        print("No open issues found.")
        return

    issue = None

    for item in issues:
        if "pull_request" not in item:
            issue = item
            break

    if issue is None:
        print("No eligible issues found.")
        return

    execute_issue(issue)


if __name__ == "__main__":
    run_execution_cycle()