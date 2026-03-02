import os
from devin_automation.classifier import classify_batch
from devin_automation.github_client import (
    fetch_open_issues,
    label_issue,
    post_comment,
    set_devin_status,
    send_slack
)
from devin_automation.issue_runner import execute_issue

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def apply_triage(issue_number, classification):
    difficulty = classification["difficulty"]
    summary = classification["summary"]
    recommended_action = classification["recommended_action"]
    reason = classification["reason"]

    # existing_labels = get_issue_labels(issue_number)
    # for label in existing_labels:
    #     if label.startswith("devin-"):
    #         remove_label(issue_number, label)

    label_issue(issue_number, f"devin-{difficulty}")

    comment_body = f"""
 **Devin Triage Summary**

**Summary**
{summary}

**Estimated Difficulty** {difficulty.capitalize()}

**Recommended Action**
{recommended_action}

**Reasoning**
{reason}

"""

    post_comment(issue_number, comment_body)


def main():
    print("Starting Devin backlog automation...\n")

    label = os.environ.get("ISSUE_LABEL", "")
    if label and label != "devin-fix":
        print("Label not eligible. Skipping.")
        return

    issue_number = os.environ.get("ISSUE_NUMBER")
    issues = fetch_open_issues(limit=50)
    issues = [i for i in issues if "pull_request" not in i]
    issues = [i for i in issues if not any(l["name"] == "devin-status: completed" for l in i.get("labels", []))]


    if not issues:
        print("No open issues found.")
        return

    if issue_number:
        issues_to_run = [i for i in issues if str(i["number"]) == str(issue_number)]
    else:
        issues_to_run = issues[:5]
        
    for issue in issues_to_run:
        set_devin_status(issue["number"], "running")

    send_slack(f"🚀 Devin automation started — processing {len(issues_to_run)} issue(s)")

    print(f"Processing {len(issues_to_run)} issues...\n")
    pr_count = 0
    flagged_count = 0
    pr_urls = []
    
    for chunk in chunk_list(issues_to_run, 10):
        # time.sleep(3)
        results = classify_batch(chunk)
        result_map = {r["issue_number"]: r for r in results}

        for issue in chunk:
            number = issue["number"]
            classification = result_map.get(number)

            if not classification:
                print(f"⚠️ Missing classification for issue #{number}")
                continue

            print(f"\nIssue #{number}")
            print(classification)
            
            difficulty = classification["difficulty"]
            summary = classification["summary"]

            apply_triage(number, classification)
            send_slack(f"🔍 Issue #{number} classified as *{difficulty.upper()}* — {summary}")

            if difficulty in ["easy", "medium"]:
                send_slack(f"⚙️ Devin is fixing issue #{number}...")
                pr_url = execute_issue(issue)
                pr_count += 1
                if pr_url:
                    pr_urls.append(f"• Issue #{number}: {pr_url}")
                    send_slack(f"✅ Issue #{number} — draft PR opened: {pr_url}")
            else:
                flagged_count += 1
                send_slack(f"⚠️ Issue #{number} is *{difficulty}* — flagged for senior review")
                print(f"Issue #{number} is {difficulty} - skipping execution")

    pr_links = "\n".join(pr_urls) if pr_urls else "Check GitHub for PRs"
    send_slack(f"📊 Run complete — {pr_count} PR(s) opened, {flagged_count} flagged for review\n{pr_links}")

if __name__ == "__main__":
    main()