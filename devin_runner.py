from devin.classifier import classify_batch
from devin.github_client import (
    fetch_open_issues,
    label_issue,
    post_comment,
    get_issue_labels,
    remove_label,
    set_devin_status
)
from devin.issue_runner import execute_issue
import os


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def apply_triage(issue_number, classification):
    difficulty = classification["difficulty"]
    summary = classification["summary"]
    recommended_action = classification["recommended_action"]
    reason = classification["reason"]

    existing_labels = get_issue_labels(issue_number)
    for label in existing_labels:
        if label.startswith("devin-"):
            remove_label(issue_number, label)

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

    if not issues:
        print("No open issues found.")
        return

    if issue_number:
        issues_to_run = [i for i in issues if str(i["number"]) == str(issue_number)]
    else:
        issues_to_run = issues[:5]
        
    for issue in issues_to_run:
        set_devin_status(issue["number"], "running")

    print(f"Processing {len(issues_to_run)} issues...\n")

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

            apply_triage(number, classification)

            if classification["difficulty"] in ["easy", "medium"]:
                execute_issue(issue)
            else:
                print(f"Issue #{number} is {classification['difficulty']} - skipping execution")


if __name__ == "__main__":
    main()