# devin/executor.py

from devin.github_client import (
    post_comment,
    set_devin_status,
    remove_label,
    pr_exists,
    branch_exists,
    status_is_completed,
)


from devin.devin_worker import run_issue


LABEL_IN_PROGRESS = "devin-in-progress"


def execute_issue(issue):
    issue_number = issue["number"]

    print(f"Executing issue #{issue_number}")
    if pr_exists(issue_number):
        print("PR already exists. Skipping.")
        return

    if branch_exists(issue_number):
        print("Branch already exists. Skipping.")
        return

    if status_is_completed(issue_number):
        print("Already completed. Skipping.")
        return
      
    set_devin_status(issue_number, "running")

    try:
        result = run_issue(issue)

        if result.get("status") == "completed":
            set_devin_status(issue_number, "completed")

            post_comment(issue_number, f"""
          ### 🤖 Devin Draft PR Created

          PR URL:
          {result.get("pr_url")}
          """)

        else:
            set_devin_status(issue_number, "failed")

    except Exception as e:
        print("Execution failed:", e)
        set_devin_status(issue_number, "failed")

    finally:
        # Always unlock
        remove_label(issue_number, LABEL_IN_PROGRESS)