import os
from devin_automation.classifier import classify_batch
from devin_automation.github_client import (
    fetch_open_issues,
    send_slack,
)
from devin_automation.triage_controller import process_issue


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def main():
    print("Starting Devin backlog automation...\n")

    issue_number = os.environ.get("ISSUE_NUMBER")

    issues = fetch_open_issues(limit=50)
    issues = [i for i in issues if "pull_request" not in i]
    issues = [
        i for i in issues
        if not any(l["name"] == "devin-status: completed" for l in i.get("labels", []))
    ]

    if not issues:
        print("No open issues found.")
        return

    if issue_number:
        issues_to_run = [i for i in issues if str(i["number"]) == str(issue_number)]
    else:
        issues_to_run = issues[:5]

    send_slack(f"🚀 Devin automation started — processing {len(issues_to_run)} issue(s)")

    pr_count = 0
    flagged_count = 0
    pr_urls = []

    for chunk in chunk_list(issues_to_run, 10):
        results = classify_batch(chunk)
        result_map = {r["issue_number"]: r for r in results}

        for issue in chunk:
            number = issue["number"]
            classification = result_map.get(number)

            if not classification:
                print(f"⚠️ Missing classification for issue #{number}")
                continue

            result = process_issue(issue, classification)

            if result["status"] == "completed":
                pr_count += 1
                pr_urls.append(f"• Issue #{number}: {result['pr_url']}")
            elif result["status"] == "needs_review":
                flagged_count += 1

    pr_links = "\n".join(pr_urls) if pr_urls else "Check GitHub for PRs"

    send_slack(
        f"📊 Run complete — {pr_count} PR(s) opened, "
        f"{flagged_count} flagged for review\n{pr_links}"
    )


if __name__ == "__main__":
    main()