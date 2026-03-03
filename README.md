# finserv-demo
# Devin Backlog Automation

FinServ has 300+ open issues across their monorepo, junior engineers spend more time reading context than writing code. Senior engineers are too deep in platform work to care about the backlog.

This project automates that entire pipeline — entirely within GitHub. No new tools, no new dashboards. Issues come in via GitHub, Devin fixes them, PRs land back in GitHub. Engineers just review and merge.

---

## How It Works

When triggered, the automation runs a two-step pipeline:

**Step 1 — Classify.** A Devin session reads each issue and classifies it as `easy`, `medium`, `hard`, or `unsure`. It posts a triage summary comment on the issue and applies a difficulty label. Engineers instantly know what they're dealing with.

**Step 2 — Fix.** Only `easy` and `medium` issues get routed to Devin for fixing. Devin reads the repo and the codebase, implements the fix, creates a new branch, and opens a draft PR. Hard issues are flagged for senior review — Devin leaves those alone.

This gives a deliberate balance between automation and human oversight. Devin handles the routine work. Engineers keep full control over what gets merged — nothing is ever auto-merged.

---

## Two Ways to Trigger It

**Label trigger.** Add the `devin-fix` label to any issue. The automation kicks off immediately for that specific issue — classifies it, and fixes it if eligible.

**Batch via GitHub Actions.** Run the workflow manually from the Actions tab. It picks up a number (user can determined but for this demo 5) eligible open issues and processes them in parallel.

Both modes run the same pipeline — classify first, then fix.

---

## Integration

- **Devin API** — sessions are created programmatically via the Devin API. One session for classification, a separate session per issue for the fix.
- **GitHub** — Devin is connected to the repository via the Devin GitHub integration, giving it authenticated access to create branches and open PRs. All labels, comments, and status updates are written back to GitHub via the GitHub API.
- **GitHub Actions** — the entire workflow is triggered and run inside GitHub Actions. No external infrastructure needed.
- - **Slack** — real-time notifications are posted to a Slack channel at every stage of the pipeline. Engineers are kept in the loop without leaving Slack — from automation start, to classification results, to PR opened, to run complete summary.

---

## Project Structure

`devin_runner.py` sits at the root as the orchestration layer — it coordinates classification and execution across all targeted issues. 

`devin_automation/` contains the underlying automation packages. 

`finserv_core/` is the demo application and can be swapped out for any real codebase.
```
finserv-demo/
├── .github/
│   └── workflows/
│       └── devin.yml           # GitHub Actions workflow — triggers on label or manual run
│
├── devin_automation/           # Automation package
│   ├── classifier.py           # Classifies issues via Devin structured output
│   ├── issue_runner.py         # Manages the lifecycle of each issue
│   ├── devin_worker.py         # Builds the fix prompt and calls Devin
│   ├── devin_client.py         # Devin API client
│   └── github_client.py        # GitHub API client
│   └── triage_classifier.py    # Orchestrates triage and routes to execution
│
├── finserv_core/               # Demo application — can be any repo or codebase
│
├── devin_runner.py             # Entry point — runs the full pipeline
└── README.md
```
---

## Issue Labels

| Label | What it means |
|---|---|
| `devin-fix` | Trigger automation on this issue |
| `devin-easy` | Small, localised fix |
| `devin-medium` | Moderate complexity |
| `devin-hard` | Too complex — flagged for senior review |
| `devin-unsure` | Not enough info to classify |
| `devin-status: running` | Pipeline is active |
| `devin-status: completed` | Draft PR is open |
| `devin-status: failed` | Devin couldn't complete the fix |
| `devin-status: needs review` | Manual Review needed |

---

## Setup

**1. Add your Devin API key to GitHub Secrets**

Repo → Settings → Secrets → Actions → `DEVIN_API_KEY`

Get your key at [app.devin.ai/settings/api-keys](https://app.devin.ai/settings/api-keys)

**2. Connect Devin to your repo**

[app.devin.ai](https://app.devin.ai) → Settings → Integrations → GitHub

**3. Create the labels**

`devin-fix`, `devin-easy`, `devin-medium`, `devin-hard`, `devin-unsure`, `devin-status: running`, `devin-status: completed`, `devin-status: failed`

**4. Trigger**

Add `devin-fix` to an issue, or run the workflow manually from the Actions tab.
