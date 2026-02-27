from devin.classifier import classify_batch
from devin.github_client import (
    fetch_open_issues,
    label_issue,
    post_comment,
    get_issue_labels,
    remove_label
)
from devin.classifier import classify_batch

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def apply_triage(issue_number, classification):
    difficulty = classification["difficulty"]
    summary = classification["summary"]
    recommended_action = classification["recommended_action"]
    reason = classification["reason"]

    # Remove existing devin-* labels
    existing_labels = get_issue_labels(issue_number)
    for label in existing_labels:
        if label.startswith("devin-"):
            remove_label(issue_number, label)

    # Apply fresh label
    label_issue(issue_number, f"devin-{difficulty}")

    # Post updated triage comment
    comment_body = f"""
🤖 **Devin Triage Summary**

**Summary**
{summary}

**Estimated Effort**
{difficulty.capitalize()}

**Recommended Action**
{recommended_action}

**Reasoning**
{reason}

---

If you'd like Devin to proceed, add the `devin-approve` label.
"""

    post_comment(issue_number, comment_body)

def main():
    print("🚀 Starting Devin triage automation...\n")

    issues = fetch_open_issues(limit=20)
    print(f"Found {len(issues)} open issues.\n")

    for chunk in chunk_list(issues, 10):
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


if __name__ == "__main__":
    main()