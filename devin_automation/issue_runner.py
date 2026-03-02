from devin_automation.github_client import (
    remove_label,
    pr_exists,
    branch_exists,
    status_is_completed,
    get_issue_labels
)
from devin_automation.devin_worker import run_issue

LABEL_IN_PROGRESS = "devin-in-progress"

def execute_issue(issue):
    issue_number = issue["number"]

    print(f"Executing issue #{issue_number}")

    if pr_exists(issue_number):
        print("PR already exists. Skipping.")
        return {"status": "already_completed", "pr_url": None}

    if branch_exists(issue_number):
        print("Branch already exists. Skipping.")
        return {"status": "already_completed", "pr_url": None}

    if status_is_completed(issue_number):
        print("Already completed. Skipping.")
        return {"status": "already_completed", "pr_url": None}

    existing_labels = get_issue_labels(issue_number)

    try:
        result = run_issue(issue)

        if result and result.get("status") == "completed":

            if "devin-fix" in existing_labels:
                remove_label(issue_number, "devin-fix")

            return {
                "status": "completed",
                "pr_url": result.get("pr_url")
            }

        if "devin-fix" in existing_labels:
            remove_label(issue_number, "devin-fix")

        return {"status": "failed", "pr_url": None}

    except Exception as e:
        print("Execution failed:", e)

        if "devin-fix" in existing_labels:
            remove_label(issue_number, "devin-fix")

        return {"status": "failed", "pr_url": None}

    finally:
        remove_label(issue_number, LABEL_IN_PROGRESS)