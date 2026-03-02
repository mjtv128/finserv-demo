from devin_automation.github_client import (
    set_devin_status,
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
        return

    if branch_exists(issue_number):
        print("Branch already exists. Skipping.")
        return

    if status_is_completed(issue_number):
        print("Already completed. Skipping.")
        return
      
    # set_devin_status(issue_number, "running")

    try:
        result = run_issue(issue)

        if result.get("status") == "completed":
            set_devin_status(issue_number, "completed")
            
            existing_labels = get_issue_labels(issue_number)
            if "devin-fix" in existing_labels:
                remove_label(issue_number, "devin-fix")
            return result.get('pr_url')

        else:
            set_devin_status(issue_number, "failed")

    except Exception as e:
        print("Execution failed:", e)
        set_devin_status(issue_number, "failed")

    finally:
        remove_label(issue_number, LABEL_IN_PROGRESS)