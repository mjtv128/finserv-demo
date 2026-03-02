from devin_automation.github_client import (
    label_issue,
    post_comment,
    set_devin_status,
    send_slack,
)
from devin_automation.issue_runner import execute_issue

def process_issue(issue, classification):
    number = issue["number"]
    difficulty = classification["difficulty"]
    summary = classification["summary"]
    recommended_action = classification["recommended_action"]
    reason = classification["reason"]

    set_devin_status(number, "running")

    label_issue(number, f"devin-{difficulty}")

    body = f"""
    **Devin Triage Summary**

    **Summary**
    {summary}

    **Estimated Difficulty** {difficulty.capitalize()}

    **Action**
    {recommended_action}

    **Reason**
    {reason}
    """
    post_comment(number, body)

    send_slack(
        f"🔍 Issue #{number} classified as *{difficulty.upper()}* — {summary}"
    )

    if difficulty in ["easy", "medium"]:
        send_slack(f"⚙️ Devin is fixing issue #{number}...")
        pr_url = execute_issue(issue)

        if pr_url:
            set_devin_status(number, "completed")
            send_slack(f"✅ Issue #{number} — draft PR opened: {pr_url}")
            return {"status": "completed", "pr_url": pr_url}
        else:
            set_devin_status(number, "needs review")
            return {"status": "failed"}

    else:
        set_devin_status(number, "needs review")
        send_slack(f"⚠️ Issue #{number} flagged for senior review")
        return {"status": "needs_review"}