from devin.github_client import (
    fetch_open_issues,
    count_open_devin_prs,
    label_issue,
    remove_label,
    post_comment,
    get_default_branch_sha,
    create_branch,
    create_or_update_file,
    create_draft_pr,
)

MAX_OPEN_DEVIN_PRS = 5


def run_execution_cycle():
    print("🚀 Starting execution cycle")

    open_prs = count_open_devin_prs()
    print("Open Devin PRs:", open_prs)

    if open_prs >= MAX_OPEN_DEVIN_PRS:
        print("Max PR limit reached.")
        return

    issues = fetch_open_issues(limit=20)

    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", [])]

        if "devin-easy" not in labels and "devin-medium" not in labels:
            continue

        if "devin-in-progress" in labels:
            continue

        execute_issue(issue)
        break


def execute_issue(issue):
    issue_number = issue["number"]

    print(f"Executing issue #{issue_number}")

    label_issue(issue_number, "devin-in-progress")
    post_comment(issue_number, "🤖 Devin execution started.")

    sha, base_branch = get_default_branch_sha()
    branch_name = f"devin/issue-{issue_number}"

    create_branch(branch_name, sha)

    create_or_update_file(
        path=f"devin_test_{issue_number}.txt",
        content="Test change from Devin execution layer.",
        branch=branch_name,
        message=f"Devin test commit for issue #{issue_number}"
    )

    pr = create_draft_pr(
        title=f"[Devin] Test PR for issue #{issue_number}",
        body="Auto-generated draft PR.",
        head_branch=branch_name,
        base_branch=base_branch
    )

    print("PR created:", pr["html_url"])

    remove_label(issue_number, "devin-in-progress")


if __name__ == "__main__":
    run_execution_cycle()