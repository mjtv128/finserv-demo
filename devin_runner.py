from devin.github_client import fetch_open_issues, label_issue
from devin.classifier import classify_batch


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


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

            label = (
                "auto-safe"
                if classification["automation_category"] == "safe"
                else "needs-review"
            )

            label_issue(number, label)


if __name__ == "__main__":
    main()