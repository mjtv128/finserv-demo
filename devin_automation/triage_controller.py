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

    # set_devin_status(number, "running")
    label_issue(number, f"devin-{difficulty}")

    body = (
        f"**Devin Triage Summary**\n\n"
        f"**Summary**\n"
        f"{summary}\n\n"
        f"**Estimated Difficulty** {difficulty.capitalize()}\n\n"
        f"**Action**\n"
        f"{recommended_action}\n\n"
        f"**Reason**\n"
        f"{reason}"
    )

    post_comment(number, body)

    send_slack(
        f"🔍 Issue #{number} classified as *{difficulty.upper()}* — {summary}"
    )

    if difficulty in ["easy", "medium"]:
        send_slack(f"⚙️ Devin is fixing issue #{number}...")
        result = execute_issue(issue)

        if result["status"] in ["completed", "already_completed"]:
            set_devin_status(number, "completed")

            if result["pr_url"]:
                send_slack(f"✅ Issue #{number} — draft PR opened: {result['pr_url']}")
            else:
                send_slack(f"ℹ️ Issue #{number} already had a PR.")

            return {
                "final_status": "completed",
                "pr_url": result["pr_url"]
            }

        elif result["status"] == "failed":
            set_devin_status(number, "needs review")
            return {"final_status": "needs_review", "pr_url": None}

    else:
        set_devin_status(number, "needs review")
        send_slack(f"⚠️ Issue #{number} flagged for senior review")
        return {"final_status": "needs_review", "pr_url": None}