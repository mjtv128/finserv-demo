# devin/fix_issues.py

from devin.github_client import (
    fetch_open_issues,
    label_issue,
    remove_label,
    post_comment
)

from devin.devin_worker import run_issue


def run_execution_cycle():
    print("🚀 Starting execution cycle")

    issues = fetch_open_issues(limit=10)

    if not issues:
        print("No open issues found.")
        return

    # Take the first issue only
    issue = None

    for item in issues:
        if "pull_request" not in item:
            issue = item
            break

    if issue is None:
        print("No eligible issues found.")
        return
    issue_number = issue["number"]
    labels = [l["name"] for l in issue.get("labels", [])]

    print(f"Checking issue #{issue_number}")

    if "devin-easy" not in labels and "devin-medium" not in labels:
        print("Issue not eligible for execution.")
        return

    if "devin-in-progress" in labels:
        print("Issue already in progress.")
        return

    print(f"Executing issue #{issue_number}")

    label_issue(issue_number, "devin-in-progress")
    post_comment(issue_number, "🤖 Devin execution started.")

    try:
      result = run_issue(issue)

      if result["status"] == "completed":
          print("PR created:", result["pr_url"])

          post_comment(issue_number, f"""
  ### 🤖 Devin Draft PR Created

  Draft PR:
  {result["pr_url"]}
  """)

      else:
          print("Execution failed.")

    except Exception as e:
        print("Execution failed:", e)

    finally:
        remove_label(issue_number, "devin-in-progress")


if __name__ == "__main__":
    run_execution_cycle()