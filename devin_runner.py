from devin.github_client import fetch_open_issues, label_issue
from devin.classifier import classify_batch


def determine_automation_policy(difficulty, risk):
    # Simple rule:
    # High risk or hard changes should not be automated.
    if risk == "high" or difficulty == "hard":
        return "manual"
    return "automatable"


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def apply_triage_labels(issue_number, classification):
    difficulty = classification["difficulty"]
    risk = classification["risk_level"]
    scope = classification["scope"]

    readiness = determine_automation_policy(difficulty, risk)

    labels = [
        f"devin-difficulty-{difficulty}",
        f"devin-risk-{risk}",
        f"devin-scope-{scope}",
        f"devin-{readiness}"
    ]

    for label in labels:
        label_issue(issue_number, label)

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

            apply_triage_labels(number, classification)


if __name__ == "__main__":
    main()