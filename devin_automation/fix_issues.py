import os
from devin_automation.github_client import fetch_open_issues
from devin_automation.issue_runner import execute_issue
from concurrent.futures import ThreadPoolExecutor

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
        issue = next((i for i in issues if str(i["number"]) == str(issue_number) and "pull_request" not in i), None)
        if not issue:
          print(f"Issue #{issue_number} not found.")
          return
        execute_issue(issue)
        
    else:
        issues_to_run = [i for i in issues if "pull_request" not in i][:5]
        if not issues_to_run:
            print("No issues issues found.")
            return
        print(f"Found {len(issues_to_run)} issues. Running in parallel...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(execute_issue, issues_to_run)



if __name__ == "__main__":
    run_execution_cycle()