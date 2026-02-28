# devin/fix_issues.py

from devin.github_client import (
    fetch_open_issues,
    label_issue,
    remove_label,
    count_open_devin_prs,
    post_comment
)

from devin.classifier import classify_batch
from devin.devin_worker import run_issue


MAX_OPEN_DEVIN_PRS = 5


def run_execution_cycle():
    print("🚀 Starting execution cycle")

    open_prs = count_open_devin_prs()
    print("Open Devin PRs:", open_prs)

    if open_prs >= MAX_OPEN_DEVIN_PRS:
        print("Max PR limit reached.")
        return

    issues = fetch_open_issues(limit=10)

    # ---- PHASE 1: TRIAGE (Batch) ----
    untriaged = []
    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", [])]
        if not any(label.startswith("devin-") for label in labels):
            untriaged.append(issue)

    if untriaged:
        print("Running batch triage")

        triage_results = classify_batch(untriaged)

        for result in triage_results:
            issue_number = result["issue_number"]
            difficulty = result["difficulty"]

            difficulty_label = f"devin-{difficulty}"
            label_issue(issue_number, difficulty_label)

            comment_body = f"""
### 🤖 Devin Triage

**Difficulty:** {difficulty}

**Summary:**  
{result['summary']}

**Recommended Action:**  
{result['recommended_action']}

**Reasoning:**  
{result['reason']}
"""

            post_comment(issue_number, comment_body)

        return  # one phase per run

    # ---- PHASE 2: EXECUTION ----
    for issue in issues:
        issue_number = issue["number"]
        labels = [l["name"] for l in issue.get("labels", [])]

        if "devin-easy" not in labels and "devin-medium" not in labels:
            continue

        if "devin-in-progress" in labels:
            continue

        print(f"Executing issue #{issue_number}")

        label_issue(issue_number, "devin-in-progress")

        try:
            # Re-triage single issue to get structured metadata
            triage = classify_batch([issue])[0]

            result = run_issue(issue, triage)
            print("Execution result:", result)

        finally:
            remove_label(issue_number, "devin-in-progress")

        return  # process one issue per run


if __name__ == "__main__":
    run_execution_cycle()