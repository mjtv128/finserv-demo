# devin/fix_issues.py

from devin.github_client import fetch_open_issues
from devin.issue_runner import execute_issue
import os

def run_execution_cycle():
    print("🚀 Starting execution cycle")
    
    label = os.environ.get("ISSUE_LABEL", "")
    if label and label != "devin-fix":
        print("Label not eligible. Skipping.")
        return

    issue_number = os.environ.get("ISSUE_NUMBER")

    issues = fetch_open_issues(limit=50)

    if not issues:
        print("No open issues found.")
        return

    if issue_number:
        # triggered by label event - fix that specific issue
        issue = next((i for i in issues if str(i["number"]) == str(issue_number) and "pull_request" not in i), None)
    else:
        # triggered manually - pick next eligible
        issue = next((i for i in issues if "pull_request" not in i), None)

    if issue is None:
        print("No eligible issues found.")
        return

    execute_issue(issue)


if __name__ == "__main__":
    run_execution_cycle()